
// Plone-specific editing scripts.  Referenced by plone/bottom.pt.
// The variable "ui_url" is provided by common/header.pt.
function plone_edit(element) {
  var path = element.getAttribute("full_path");
  window.document.location = path + "/edit_compo_element"; 
}

function plone_add(e, target) {
  // Note that target_index is also available.
  var target_path = target.getAttribute("target_path");
  var target_index = target.getAttribute("target_index");
  draweropen(e, target_path, target_index);
}

function plone_add_ajax(e, target) {
  // Note that target_index is also available.
  var target_path = target.getAttribute("target_path");
  var target_index = target.getAttribute("target_index");
  var target_id = target.getAttribute("id");
  draweropen_ajax(e, target_path, target_index, target_id);
}

function plone_add_title(target) {
  // Note that target_index is also available.
  var form = document.forms.modify_composites;
  var compopage_path = form.elements.composite_path.value;
  var title = prompt('Input the title value', 'a title');
  var target_path = target.getAttribute("target_path");
  var target_index = target.getAttribute("target_index");
  url = "createCompoTitle?target_path=" + target_path;
  url = url + "&target_index=" + target_index;
  url = url + "&compopage_path=" + compopage_path;
  url = url + "&title=" + title;
  window.document.location = url;
}

function plone_add_ajax_title(target) {
  // Note that target_index is also available.
  var form = document.forms.modify_composites;
  var compopage_path = form.elements.composite_path.value;
  var title = prompt('Input the title value', 'a title');
  var target_path = target.getAttribute("target_path");
  var target_index = target.getAttribute("target_index");
  var id = target.getAttribute("id");
  url = compopage_path + '/cp_container/addTitle';
  params = "target_path=" + target_path;
  params = params + "&target_index=" + target_index;
  params = params + "&compopage_path=" + compopage_path;
  params = params + "&title=" + title;
  params = params + "&target_id=" + id;
  kukit.notifyServerWithParams(url, params);
}

function plone_add_ajax_fragment(target) {
  // Note that target_index is also available.
  var form = document.forms.modify_composites;
  var compopage_path = form.elements.composite_path.value;
  var target_path = target.getAttribute("target_path");
  var target_index = target.getAttribute("target_index");
  var id = target.getAttribute("id");
  url = compopage_path + '/cp_container/addFragment';
  params = "target_path=" + target_path;
  params = params + "&target_index=" + target_index;
  params = params + "&compopage_path=" + compopage_path;
  params = params + "&target_id=" + id;
  kukit.notifyServerWithParams(url, params);
}

function plone_add_fragment(target) {
  // Note that target_index is also available.
    var form = document.forms.modify_composites;
    var compopage_path = form.elements.composite_path.value;
    var target_path = target.getAttribute("target_path");
    var target_index = target.getAttribute("target_index");
    url = "createCompoFragment?target_path=" + target_path;
    url = url + "&target_index=" + target_index;
    url = url + "&compopage_path=" + compopage_path;
    window.document.location = url;
}

function plone_add_portlet(target) {
  // Note that target_index is also available.
    var form = document.forms.modify_composites;
    var compopage_path = form.elements.composite_path.value;
    var target_path = target.getAttribute("target_path");
    var target_index = target.getAttribute("target_index");
    url = "createCompoPortlet?target_path=" + target_path;
    url = url + "&target_index=" + target_index;
    url = url + "&compopage_path=" + compopage_path;
    window.document.location = url;
}

function plone_change_viewlet(element, viewlet) {
  var form, url, element_path, compopage_path;
  form = document.forms.modify_composites;
  compopage_path = form.elements.composite_path.value;
  element_path = element.getAttribute("full_path");
  url = element_path + "/change_viewlet?viewletId=" + viewlet;
  url = url + "&compopage_path=" + compopage_path;
  window.document.location = url;
}


function composite_pack_prepare_element_menu(header) {
  var allowed_viewlets_titles, allowed_viewlets_ids;
  var current_viewlet_id;
  if (!pd_selected_item) {
    allowed_viewlets_ids = null;
    allowed_viewlets_titles = null;
    current_viewlet_id = null;
  }
  else {
    allowed_viewlets_ids = pd_selected_item.getAttribute('allowed_viewlets_ids');
    allowed_viewlets_titles = pd_selected_item.getAttribute('allowed_viewlets_titles');
    current_viewlet_id = pd_selected_item.getAttribute('current_viewlet_id');
}
  header.parentNode.setAttribute("allowed_viewlets_ids", allowed_viewlets_ids);
  header.parentNode.setAttribute("allowed_viewlets_titles", allowed_viewlets_titles);
  header.parentNode.setAttribute("current_viewlet_id", current_viewlet_id);
  composite_prepare_element_menu(header);
  return true;
}

function composite_prepare_change_viewlet_menu(header) {
    // Prepares the header of the element context menu.
    var node, menuItem, i, parent;
    var viewlets_titles, viewlets_ids;
    var current_viewlet_id;

    while (header.childNodes.length)
        header.removeChild(header.childNodes[0]);
        
    parent = header.parentNode;
    if (parent.getAttribute("allowed_viewlets_ids")) {
        viewlets_ids = parent.getAttribute("allowed_viewlets_ids").split(" ");
        viewlets_titles = parent.getAttribute("allowed_viewlets_titles").split("%");
        current_viewlet_id = parent.getAttribute("current_viewlet_id");
        if (viewlets_ids.length != 0) { 
            // change viewlet header
            menuItem = document.createElement("div");
            menuItem.className = "context-menu-header";
            select_header = getNodeHeaderTitle(header, "Select Viewlet");
            node = document.createTextNode(select_header);
            menuItem.appendChild(node);
            header.appendChild(menuItem);
            // loop on viewlets
            for (i = 0; i < viewlets_ids.length; i++) {
                menuItem = document.createElement("div");
                plone_setup_viewlet_menu_item(menuItem, current_viewlet_id, viewlets_ids[i], viewlets_titles[i]);
                header.appendChild(menuItem);
            }
        }
    }
    return true;
}

function plone_setup_viewlet_menu_item(menuItem, current_id, viewlet_id, viewlet_title) {
      if (current_id == viewlet_id) {
          menuItem.id = "current-viewlet";
      }
      menuItem.className = "context-menu-item";
      menuItem.onmouseup = function() {
          plone_change_viewlet(pd_selected_item, viewlet_id);
      };
      node = document.createTextNode(viewlet_title);
      menuItem.appendChild(node);
      pd_setupContextMenuItem(menuItem);
}

function plone_updateAfterAdd(results)
{
  plone_setUpSlotElement(results[0]);
  plone_setUpSlotTarget(results[2]);
}

function plone_setUpSlotElement(node) {
    setUpSlotElement(node);
    node.onmouseout = function() {
        if (!pd_drag_event) {
            pd_highlight(node, 0);
        };
    };
    node.onmouseover = function() {
    if (!pd_drag_event) {
            pd_highlight(node, 1);
        };
    };
}

pd_node_setup['slot_element'] = plone_setUpSlotElement;

function plone_setUpSlotTarget(node) {
    var PackSetup = node.getAttribute('PackSetup');
    if (!PackSetup) {
        setup_pack_slot_target(node);
    };
    setUpSlotTarget(node);
    node.onmouseover = function() {
        pd_highlight(node, 1);
        return pd_setHighlightedTarget(node);
    };
    node.onmouseout = function() {
        pd_highlight(node, 0);
        pd_unhighlightTarget();
    };
}

function getNodeHeaderTitle(node, default_value) {
    if (node.getAttribute("header_title")) {
        return node.getAttribute("header_title");
    }
    else {
        return default_value;
    }
}

function setup_pack_slot_target(node) {
    node.setAttribute('PackSetup', '1');
    title_node = document.getElementById("slot-target-context-menu");
    header_title = getNodeHeaderTitle(title_node, "Add item");
    var menuItem = document.createElement("div");
    menuItem.className = "contentActions";
    var ul = document.createElement("ul");
    var li = document.createElement("li");
    var div = document.createElement("div");
    div.className = "menuPosition";
    var link = document.createElement("a");
    link.setAttribute("href", "#");
    var child = document.createTextNode(header_title.replace(' ', '\xa0'));
    link.appendChild(child);
    div.appendChild(link);
    li.appendChild(div);
    ul.appendChild(li);
    menuItem.appendChild(ul);
    node.appendChild(menuItem);
}

pd_node_setup['slot_target'] = plone_setUpSlotTarget;


