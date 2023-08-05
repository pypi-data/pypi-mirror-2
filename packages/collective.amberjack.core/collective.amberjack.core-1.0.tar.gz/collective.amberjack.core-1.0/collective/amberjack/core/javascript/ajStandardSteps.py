ajStandardSteps = (
    ('link', ''),  # click on the link: need a selector to <a>
    ('button', ''),  # click on the button: need a selector to a <input type="button|submit|reset|...">
    ('collapsible', ''), # if [value] is "collapse", switch the class of the element from expandedInlineCollapsible to collapsedInlineCollapsible, else the contrary
    ('select', ''),  # replace the value of the element
    ('text', ''),  # replace the value of the element
    ('checkbox', ''),  # if [value] is "checked", then check the element, else uncheck
    ('radio', ''),  # if [value] is "checked", then check the element, else uncheck
    ('multiple_select', ''),  # select the options with value given by [value] (can be a list separated by coma without space)
    
    ('tiny_button_exec',''),
    ('tiny_button_click',''),
    ('iframe_click',''),
    ('iframe_text',''),
    
    ('manage_portlets', 'div.managePortletsLink a'),
    
    ('go_home', '#portal-breadcrumbs > a'),
    ('go_uplevel', '#portal-breadcrumbs span a:last'),
    
    ('site_sitemap', '#siteaction-sitemap a'),
    ('site_accessibility', '#siteaction-accessibility a'),
    ('site_contact', '#siteaction-contact a'),
    ('site_setup', '#siteaction-plone_setup a'),
    
    ('action_cut', '#cut'),
    ('action_copy', '#copy'),
    ('action_delete', '#delete'),
    ('action_rename', '#rename'),
    
    ('new_folder', '#folder'),
    ('new_link', '#link'),
    ('new_event', '#event'),
    ('new_image', '#image'),
    ('new_news', '#news-item'),
    ('new_document', '#document'),
    ('new_file', '#file'),
    
    ('view_standard', '#folder_listing'),
    ('view_summary', '#folder_summary_view'),
    ('view_tabular', '#folder_tabular_view'),
    ('view_thumbnail', '#atct_album_view'),
    
    ('default_page', '#contextSetDefaultPage'),
    
    ('contentview_content', '#contentview-folderContents a'),
    ('contentview_view', '#contentview-view a'),
    ('contentview_edit', '#contentview-edit a'),
    ('contentview_rules', '#contentview-contentrules a'),
    ('contentview_sharing', '#contentview-local_roles a'),
    
    ('content_publish', '#workflow-transition-publish'),
    ('content_sendback', '#workflow-transition-reject'),
    
    ('form_apply', '#form\\.actions\\.apply'),
    ('form_save', 'input[name=form\\.button\\.save]'),  # in Archetypes >= 1.5.11 (Plone >= 3.2.3)
    ('form_save_default_page', 'input[name=form\\.button\\.Save]'),  # in contextSetDefaultPage there's a capital letter 
    ('form_actions_save', 'input[name=form\\.actions\\.save]'), #BBB has problems
    ('form_remove', 'input[name=form\\.button\\.remove]'),
    ('form_cancel', 'input[name=form\\.button\\.cancel]'),
    
    ('form_title', '#archetypes-fieldname-title input'),
    ('form_description', '#archetypes-fieldname-description textarea'),
    ('form_text', '#text_ifr'),
    ('form_location', '#archetypes-fieldname-location input'),
    ('form_url', '#remoteUrl'),
    
    ('form_header', 'input[id="form\\.header"]'),
    ('form_footer', 'input[id="form\\.footer"]'),
    
    ('folder_copy', 'input[name="folder_copy:method"]'),
    ('folder_cut', 'input[name="folder_cut:method"]'),
    ('folder_paste', 'input[name="folder_paste:method"]'),
    ('folder_delete', 'input[name="folder_delete:method"]'),
    ('folder_rename', 'input[name="folder_rename_form:method"]'),
    ('content_status_history', 'input[name="content_status_history:method"]'),
    
    ('image_title', '#title'),
    ('image_description', '#description'),
    ('image_file', '#image_file'),
    ('image_save', '.formControls input.context'),
    ('file_file', '#file_file'),
    
    ('button_dialog_ok', '#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button'), # there are 3 buttons of the same kind
    ('button_dialog_cancel', '#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button'), # there are 3 buttons of the same kind
    ('button_dialog_reload', '#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button'), # there are 3 buttons of the same kind
    ('image_align_left', '#image-align-left'),
    
    ('calendar_next', '#calendar-next'),
    ('calendar_previous', '#calendar-previous'),
    ('subtype_videocontainer', '#IVideoContainerEnhanced'),
    
    ('menu_sub-types', '#subtypes'),
    ('menu_display', '#plone-contentmenu-display'),
    ('menu_add-new', '#plone-contentmenu-factories'),
    ('menu_state', '#plone-contentmenu-workflow'),
   
)


