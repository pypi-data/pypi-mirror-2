## Controller Python Script "prefs_simpleblog_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=publishedState='published', createPortletOnBlogCreation=None, globalCategories='', allowAnonymousViewByline=None, showRecent=None, showComments=None, showCategories=None, showCalendar=None
##title=Setup SimpleBlog

context.simpleblog_tool.setProperties(publishedState, 
                                                      createPortletOnBlogCreation, 
                                                      globalCategories, 
                                                      allowAnonymousViewByline,
                                                      showRecent,
                                                      showCalendar,
                                                      showCategories,
                                                      showComments)

return state.set(portal_status_message='SimpleBlog configured.')
