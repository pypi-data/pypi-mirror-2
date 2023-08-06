import logging
from zope.app.component.interfaces import ISite

from plumi.app.vocabs  import vocab_set as vocabs
from plumi.app.config import TOPLEVEL_TAXONOMY_FOLDER , GENRE_FOLDER, CATEGORIES_FOLDER, COUNTRIES_FOLDER, SUBMISSIONS_FOLDER, SE_ASIA_COUNTRIES

#imports from old style plone 'Products' namespace
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.Five.component import enableSite
from Products.CMFPlone.interfaces import IPropertiesTool

from zope.component import getUtility , queryUtility
from zope.component import getMultiAdapter
from zope.app.container.interfaces import INameChooser
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping, ILocalPortletAssignmentManager
from plone.portlet.collection.collection import Assignment
from plone.app.discussion.interfaces import ICommentingTool
from plone.app.discussion.interfaces import IConversation

from AccessControl import allow_module
allow_module('plumi.app.member_area.py')

#i18n
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("plumi")
from plumi.app.translations import createTranslations, deleteTranslations

#upgrade
from hashlib import md5
from datetime import datetime
from StringIO import StringIO
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from collective.transcode.star.interfaces import ITranscodeTool
from DateTime import DateTime
from Products.CMFCore.interfaces import IPropertiesTool

def initialize(context):  
    """Initializer called when used as a Zope 2 product."""
    logger=logging.getLogger('plumi.app')
    logger.debug('beginning initialize')
    # this is called at Zope instance startup, ie not installation.
    logger.debug('ending  initialize')

def app_installation_tasks(self, reinstall=False):
    """Custom Plumi setup code"""
    logger=logging.getLogger('plumi.app')
    logger.info('starting app_installation_tasks. self is %s' %self)
    portal=getToolByName(self,'portal_url').getPortalObject()
    if not ISite.providedBy(portal):
        enableSite(portal)
    
    setupRSS(portal, logger)
    setupCollections(portal, logger)
    setupDocuments(portal, reinstall, logger)

def publishObject(wftool,obj):
    logger=logging.getLogger('plumi.app')
    try:
        logger.info('publishing %s ' % obj)
        wftool.doActionFor(obj,action='publish')
    except WorkflowException:
        logger.error('caught workflow exception!') 
        pass


def setupDocuments(self, reinstall, logger):
    
    wftool = getToolByName(self,'portal_workflow')

    #Avoid doing all the following when reinstalling
    if not reinstall:
        # Taxonomy - smart folder hierarchy setup - genres/categories/countries/ 
        #    for videos we automatically [RE]create collections , hierarchically, 
        #    for all available vocabulary items
        #
        logger.info('starting taxonomy hierarchy setup')

        #delete the taxonomy folder and it's translations.
        #this should also delete all children and children's children etc
        try:
            canon = getattr(self, 'taxonomy')
            deleteTranslations(canon)
            self.manage_delObjects(['taxonomy'])
        except:
            pass
        self.invokeFactory('Folder', id = TOPLEVEL_TAXONOMY_FOLDER,
                           title = _(u'Browse Content'),
    #                      description = _(u'The top-level taxonomy of the content')
                           )
        taxonomy_fldr = getattr(self,TOPLEVEL_TAXONOMY_FOLDER,None) 
        # we start in 'taxonomy', and shld already have sub-folders constructed
        #    to hold the topics objects (smart folders), via generic setup XML
        publishObject(wftool,taxonomy_fldr)

        createTranslations(self,taxonomy_fldr)
        layout_name = "video_listing_view"


        #
        # 1 of 4: video genre
        #
        taxonomy_fldr.invokeFactory('Folder', id=GENRE_FOLDER, 
                                    title=_(u'Video Genres'))
        genre_fldr = getattr(taxonomy_fldr, GENRE_FOLDER,None)
        publishObject(wftool,genre_fldr)
        createTranslations(self,genre_fldr)
        #description string for new smart folders
        for vocab in vocabs['video_genre']:
            new_smart_fldr_id = vocab[0]
            #make the new SmartFolder
            genre_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=vocab[1])
            fldr = getattr(genre_fldr,new_smart_fldr_id)
             
            # Filter results to Plumi Video
            type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
            #Have to use the name of the Title of the Type you want to filter.
            type_criterion.setValue("Video")
             
            # Filter results to this individual genre
            type_criterion = fldr.addCriterion('getGenre', 'ATSimpleStringCriterion' )
            #match against the ID of the vocab term. see getGenre in content types 
            type_criterion.setValue(vocab[0])
            ## add criteria for showing only published videos
            state_crit = fldr.addCriterion('review_state', 'ATListCriterion')
            state_crit.setValue(['published','featured'])
            
            #XXX used to have a custom getFirstPublishedTransitionTime 
            #sort on reverse date order, using the first published time transition
            sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
            sort_crit.setReversed(True)

            #make the folder published
            fldr.setLayout(layout_name)
            publishObject(wftool,fldr)
            createTranslations(self,fldr)

        #
        # 2 of 4: video categories aka topic
        #
        taxonomy_fldr.invokeFactory('Folder',id=CATEGORIES_FOLDER,
                                    title=_(u'Video Topics'))
        categ_fldr = getattr(taxonomy_fldr, CATEGORIES_FOLDER,None)
        publishObject(wftool,categ_fldr)
        createTranslations(self,categ_fldr)

        for vocab in vocabs['video_categories']:
            new_smart_fldr_id = vocab[0]

            #make the new SmartFolder
            categ_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=vocab[1])
            fldr = getattr(categ_fldr,new_smart_fldr_id)

            # Filter results to Plumi Video
            type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
            type_criterion.setValue("Video")
            # Filter results to this individual category
            type_criterion = fldr.addCriterion('getCategories', 'ATListCriterion' )
            #match against the ID of the vocab term. see getCategories in content objects
            type_criterion.setValue(vocab[0])
            #match if any vocab term is present in the video's selected categories
            type_criterion.setOperator('or')
            ## add criteria for showing only published videos
            state_crit = fldr.addCriterion('review_state', 'ATListCriterion')
            state_crit.setValue(['published','featured'])
            #sort on reverse date order
            #XXX old getfirstpublishedtransition time 
            sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
            sort_crit.setReversed(True)

            #make the folder published.
            fldr.setLayout(layout_name)
            publishObject(wftool,fldr)
            createTranslations(self,fldr)


        #
        # 3 of 4: video countries
        #
       
        #Countries
        #get the countries from the country vocab!

        taxonomy_fldr.invokeFactory('Folder',id=COUNTRIES_FOLDER,
                                    title=_(u'Countries'))
        countries_fldr = getattr(taxonomy_fldr,COUNTRIES_FOLDER,None)
        publishObject(wftool,countries_fldr)
        createTranslations(self,countries_fldr)

        for country in vocabs['video_countries']:
            new_smart_fldr_id = country[0]

            # maybe it already exists?
            try: 
                # make the new SmartFolder
                countries_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=country[1]) 
                fldr = getattr(countries_fldr,new_smart_fldr_id)

                # Filter results to  Plumi Video
                type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
                type_criterion.setValue("Video")

                # Filter results to this individual category
                type_criterion = fldr.addCriterion('getCountries', 'ATListCriterion' )
                #
                #match against the ID of the vocab term. see getCategories in content objects
                type_criterion.setValue(country[0])
                #match if any vocab term is present in the video's selected categories
                type_criterion.setOperator('or')
                ## add criteria for showing only published videos
                state_crit = fldr.addCriterion('review_state', 'ATListCriterion')
                state_crit.setValue(['published','featured'])
                #sort on reverse date order
                sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
                sort_crit.setReversed(True)
                #publish folder
                fldr.setLayout(layout_name)
                publishObject(wftool,fldr)
                createTranslations(self,fldr)
            except:
                # should be ok from previous installation
                pass

        #
        #4 of 4 : CallOut submission categories
        #
        topic_description_string = "CallOuts for Topic - %s "
        taxonomy_fldr.invokeFactory('Folder',id=SUBMISSIONS_FOLDER,
                                    title=_(u'Call Outs'))
        submissions_fldr = getattr(taxonomy_fldr,SUBMISSIONS_FOLDER,None)
        publishObject(wftool,submissions_fldr)
        createTranslations(self,submissions_fldr)

        for submission_categ in vocabs['submission_categories']:
            new_smart_fldr_id = submission_categ[0]

            #make the new SmartFolder
            submissions_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=submission_categ[1])
            fldr = getattr(submissions_fldr,new_smart_fldr_id)
            # Filter results to Callouts
            type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
            #the title of the type, not the class name, or portal_type 
            type_criterion.setValue("Plumi Call Out")

            # Filter results to this individual category
            type_criterion = fldr.addCriterion('getSubmissionCategories', 'ATListCriterion' )
            #
            #match against the ID of the vocab term. see getCategories in callout.py (Callout object)
            type_criterion.setValue(submission_categ[0])
            #match if any vocab term is present in the video's selected categories
            type_criterion.setOperator('or')

            ## add criteria for showing only published callouts
            state_crit = fldr.addCriterion('review_state', 'ATSimpleStringCriterion')
            state_crit.setValue(['published','featured'])
            #sort on reverse date order
            sort_crit = fldr.addCriterion('modified',"ATSortCriterion")
            sort_crit.setReversed(True)
            #publish the folder
            fldr.setLayout(layout_name)
            publishObject(wftool,fldr)
            createTranslations(self,fldr)

def setupCollections(portal, logger):
    """
       Collections for display 
       latestvideos / featured-videos / news-and-events
    """

    wftool = getToolByName(portal,'portal_workflow')

    #The front page, @@featured_videos_homepage, contains
    #links to 'featured-videos' which is a smart folder containing
    #all the videos with keyword 'featured' and 'lastestvideos'
    #which is a smart folder of the latest videos. this method will
    #simply install them.

    # Items to deploy on install.
    items = (dict(id      = 'featured-videos',
                  title   = _(u'Featured Videos'),
                  desc    = _(u'Videos featured by the editorial team.'),
                  layout  = "video_listing_view",
                  exclude = True),

             dict(id      = 'latestvideos',
                  title   = _(u'Latest Videos'),
                  desc    = _(u'Latest videos contributed by the users.'),
                  layout  = "video_listing_view",
                  exclude = False),

             dict(id      = 'news_and_events',
                  title   = _(u'News and Events'),
                  desc    = _(u'Latest news and events on the site.'),
                  layout  = "folder_summary_view",
                  exclude = True),

             dict(id      = 'callouts',
                  title   = _(u'Callouts'),
                  desc    = _(u'Latest callouts.'),
                  layout  = "folder_summary_view",
                  exclude = True),

             dict(id      = 'recent_comments',
                  title   = _(u'Recent Comments'),
                  desc    = _(u'Recent comments.'),
                  layout  = "folder_listing",
                  exclude = True),

            )

    # Items creation
    for item in items:
        try:
            canon = getattr(portal, item['id'])
            deleteTranslations(canon)
            portal.manage_delObjects([item['id']])
        except:
            ## This is nasty to silence it all
            pass

        # We create the element
        portal.invokeFactory('Topic',
                           id = item['id'],
                           title = item['title'],
                           description = item['desc'].translate({}))

        fv = getattr(portal, item['id'])
 

        # We change its ownership and wf status
        publishObject(wftool, fv)

        # Filter results to ATEngageVideo
        # Have to use the name of the Title (and ATEngageVideo will be 
        #    re-named by configATEngageVideo to Video!)
        # this will actually use ALL objects with title 'Video', which 
        #    means atm, ATEngageVideo and ATVideo
        type_criterion = fv.addCriterion('Type', 'ATPortalTypeCriterion')
        if item['id'] is 'news_and_events':
            type_criterion.setValue( ("News Item","Event") )
            sort_crit = fv.addCriterion('effective',"ATSortCriterion")          
            right = getUtility(IPortletManager, name='plone.rightcolumn')
            rightColumnInThisContext = getMultiAdapter((portal, right), IPortletAssignmentMapping)
            urltool  = getToolByName(portal, 'portal_url')
            newsCollectionPortlet = Assignment(header=u"News",
                                        limit=5,
                                        target_collection = '/'.join(urltool.getRelativeContentPath(portal.news_and_events)),
                                        random=False,
                                        show_more=True,
                                        show_dates=True)
    
            def saveAssignment(mapping, assignment):
                chooser = INameChooser(mapping)
                mapping[chooser.chooseName(None, assignment)] = assignment

            saveAssignment(rightColumnInThisContext, newsCollectionPortlet)
        elif item['id'] is 'callouts':
            date_crit = fv.addCriterion('expires','ATFriendlyDateCriteria')
            # Set date reference to now
            date_crit.setValue(0)
            # Only take events in the past
            date_crit.setDateRange('-') # This is irrelevant when the date is now
            date_crit.setOperation('more')
            type_criterion.setValue( ("Plumi Call Out") )        
            sort_crit = fv.addCriterion('effective',"ATSortCriterion")
            right = getUtility(IPortletManager, name='plone.rightcolumn')
            rightColumnInThisContext = getMultiAdapter((portal, right), IPortletAssignmentMapping)
            urltool  = getToolByName(portal, 'portal_url')
            calloutsCollectionPortlet = Assignment(header=u"Callouts",
                                        limit=5,
                                        target_collection = '/'.join(urltool.getRelativeContentPath(portal.callouts)),
                                        random=False,
                                        show_more=True,
                                        show_dates=False)
          
    
            def saveAssignment(mapping, assignment):
                chooser = INameChooser(mapping)
                mapping[chooser.chooseName(None, assignment)] = assignment
            if not rightColumnInThisContext.has_key('callouts'):    
                saveAssignment(rightColumnInThisContext, calloutsCollectionPortlet)
        elif item['id'] is 'recent_comments':
            type_criterion.setValue( ("Comment") )
            sort_crit = fv.addCriterion('created',"ATSortCriterion")
            right = getUtility(IPortletManager, name='plone.rightcolumn')
            rightColumnInThisContext = getMultiAdapter((portal, right), IPortletAssignmentMapping)
            urltool  = getToolByName(portal, 'portal_url')
            commentsCollectionPortlet = Assignment(header=u"Recent Comments",
                                        limit=5,
                                        target_collection = '/'.join(urltool.getRelativeContentPath(portal.recent_comments)),
                                        random=False,
                                        show_more=True,
                                        show_dates=True)
          
    
            def saveAssignment(mapping, assignment):
                chooser = INameChooser(mapping)
                mapping[chooser.chooseName(None, assignment)] = assignment
            if not rightColumnInThisContext.has_key('recent-comments'):
                saveAssignment(rightColumnInThisContext, commentsCollectionPortlet)
        else:
            type_criterion.setValue("Video")
            sort_crit = fv.addCriterion('effective',"ATSortCriterion")

        sort_crit.setReversed(True)

        ## add criteria for showing only published videos
        state_crit = fv.addCriterion('review_state', 'ATListCriterion')
        if item['id'] is 'featured-videos':
            state_crit.setValue(['featured'])
        else:
            state_crit.setValue(['published','featured'])

        if item['exclude'] is True:
            fv.setExcludeFromNav(True)

        if item['layout'] is not None:
            fv.setLayout(item['layout'])

        fv.reindexObject()



def plumi30to31(context, logger=None):

    catalog = getToolByName(context, 'portal_catalog')
    workflow_tool = getToolByName(context,'portal_workflow')

    # Migrate callouts
    callouts = catalog(portal_type='PlumiCallOut')
    for c in callouts:
        # Migrate callout dates
        callout=c.getObject()
        closing = callout.getClosingDate()
        if closing:
            callout.setExpirationDate(closing)
            callout.reindexObject()

        # Migrate callout workflow
        from_state = workflow_tool.getInfoFor(callout,'review_state', wf_id='plone_workflow')
        current_state = workflow_tool.getInfoFor(callout, 'review_state', wf_id='plumi_workflow')
        if current_state != from_state:
            changeWorkflowState(callout, from_state, False)

    # Migrate events
    events = catalog(portal_type='Event')
    for e in events:
        # Migrate event workflow
        event=e.getObject()
        from_state = workflow_tool.getInfoFor(event,'review_state', wf_id='plone_workflow')
        current_state = workflow_tool.getInfoFor(event, 'review_state', wf_id='plumi_workflow')
        if current_state != from_state:
            changeWorkflowState(event, from_state, False)
    # Migrate news
    news = catalog(portal_type='News Item')
    for n in news:
        # Migrate news workflow
        new=n.getObject()
        from_state = workflow_tool.getInfoFor(new,'review_state', wf_id='plone_workflow')
        current_state = workflow_tool.getInfoFor(new, 'review_state', wf_id='plumi_workflow')
        if current_state != from_state:
            changeWorkflowState(new, from_state, False)


    # Migrate Videos
    videos = catalog(portal_type='PlumiVideo')
    tt = getUtility(ITranscodeTool)
    pprop = getUtility(IPropertiesTool)
    config = getattr(pprop, 'plumi_properties', None)
    tok = 0
    fok = 0


    for video in videos:
        # Migrate video annotations
        obj = video.getObject()
        UID = obj.UID()
        if not UID:
            continue
        data = StringIO(obj.getField('video_file').get(obj).data)
        md5sum = md5(data.read()).hexdigest()
        annotations = IAnnotations(obj)
        transcode_profiles = annotations.get('plumi.transcode.profiles', {})
        for profile_name in transcode_profiles.keys():
            profile = transcode_profiles[profile_name]
            path = profile.get('path', None)
            if not path:
                continue
            address = config.videoserver_address
            objRec = tt.get(UID, None)
            if not objRec:
                tt[UID] = PersistentDict()

            fieldRec = tt[UID].get('video_file', None)
            if not fieldRec:
                tt[UID]['video_file']=PersistentDict()
            tt[UID]['video_file'][profile_name] = PersistentDict({'jobId' : None, 'address' : address,'status' : 'ok', 'start' : datetime.now(), 'md5' : md5sum, 'path': path,})
        if transcode_profiles:
            del annotations['plumi.transcode.profiles']

        # Migrate video workflow
        from_state = workflow_tool.getInfoFor(obj,'review_state', wf_id='plone_workflow')
        current_state = workflow_tool.getInfoFor(obj, 'review_state', wf_id='plumi_workflow')
        if current_state != from_state:
            changeWorkflowState(obj, from_state, False)

    # Migrated featured state
    wf = getToolByName(context, 'portal_workflow')
    featured = catalog(Subject='featured')
    for f in featured:
        try:
            obj = f.getObject()
            wf.doActionFor(obj, 'feature')
             # Map changes to the catalogs
            obj.reindexObject(idxs=['allowedRolesAndUsers', 'review_state'])
        except Exception, e:
            print "Could not feature %s" % obj

def plumi31to311(context, logger=None):

    catalog = getToolByName(context, 'portal_catalog')
    commenttool = queryUtility(ICommentingTool)
    # Reindex comments
    videos = catalog(portal_type='PlumiVideo')
    comments = 0
    for video in videos:
        obj = video.getObject()
        conversation = IConversation(obj)
        for r in conversation.getThreads():
            comment_obj = r['comment']
            commenttool.reindexObject(comment_obj)
            comments = comments + 1
    print str(comments) + 'comments updated in videos'

    callouts = catalog(portal_type='PlumiCallOut')
    comments = 0
    for callout in callouts:
        obj = callout.getObject()
        conversation = IConversation(obj)
        for r in conversation.getThreads():
            comment_obj = r['comment']
            commenttool.reindexObject(comment_obj)
            comments = comments + 1
    print str(comments) + 'comments updated in callouts'

    news = catalog(portal_type='News Item')
    comments = 0
    for news_item in news:
        obj = news_item.getObject()
        conversation = IConversation(obj)
        for r in conversation.getThreads():
            comment_obj = r['comment']
            commenttool.reindexObject(comment_obj)
            comments = comments + 1
    print str(comments) + 'comments updated in news'

    events = catalog(portal_type='Event')
    comments = 0
    for event in events:
        obj = event.getObject()
        conversation = IConversation(obj)
        for r in conversation.getThreads():
            comment_obj = r['comment']
            commenttool.reindexObject(comment_obj)
            comments = comments + 1
    print str(comments) + 'comments updated in events'


def plumi311to4(context, logger=None):

    root = getToolByName(context, 'portal_url')
    portal = root.getPortalObject()
    log = portal.plone_log
    portal_types = portal.portal_types
    Topic = portal_types.getTypeInfo("Topic")
    #link.icon_expr = '' 
    Topic.content_icon = ''
    Topic.manage_changeProperties(content_icon='', icon_expr='')
    log("Removing icon type info")


def changeWorkflowState(content, state_id, acquire_permissions=False,
                        portal_workflow=None, **kw):
    """Change the workflow state of an object
    @param content: Content obj which state will be changed
    @param state_id: name of the state to put on content
    @param acquire_permissions: True->All permissions unchecked and on riles and
                                acquired
                                False->Applies new state security map
    @param portal_workflow: Provide workflow tool (optimisation) if known
    @param kw: change the values of same name of the state mapping
    @return: None
    """

    if portal_workflow is None:
        portal_workflow = getToolByName(content, 'portal_workflow')

    # Might raise IndexError if no workflow is associated to this type
    wf_def = portal_workflow.getWorkflowsFor(content)[0]
    wf_id= wf_def.getId()

    wf_state = {
        'action': None,
        'actor': None,
        'comments': "Setting state to %s" % state_id,
        'review_state': state_id,
        'time': DateTime(),
        }

    # Updating wf_state from keyword args
    for k in kw.keys():
        # Remove unknown items
        if not wf_state.has_key(k):
            del kw[k]
    if kw.has_key('review_state'):
        del kw['review_state']
    wf_state.update(kw)

    portal_workflow.setStatusOf(wf_id, content, wf_state)

    if acquire_permissions:
        # Acquire all permissions
        for permission in content.possible_permissions():
            content.manage_permission(permission, acquire=1)
    else:
        # Setting new state permissions
        wf_def.updateRoleMappingsFor(content)

    # Map changes to the catalogs
    content.reindexObject(idxs=['allowedRolesAndUsers', 'review_state'])
    return

def setupRSS(portal, logger):
    #turn on RSS site wide
    portal_syn = getToolByName(portal,'portal_syndication',None)
    try:
        portal_syn.enableSyndication(portal)
    except Exception, e:
        #throws exceptdions if already enabled!
        pass

    # turn it on in default_member_content
    # need to loop over all folders inside this folder
    default_member_content = getattr(portal,'default_member_content',None)
    for thing in default_member_content.objectValues():
        try:
            portal_syn.enableSyndication(thing)
        except:
            #throws exceptions if already enabled!
            pass


#        createTranslations(portal,fv)

