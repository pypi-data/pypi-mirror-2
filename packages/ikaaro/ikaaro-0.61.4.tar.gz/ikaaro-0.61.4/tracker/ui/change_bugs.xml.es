<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">
  <!-- Javascript -->
  <script language="javascript">
  var list_products = {<stl:inline stl:repeat="product list_products">
                       "${product/id}":
                          {'module':
                           [<stl:inline stl:repeat="module product/modules">
                             {"id": "${module/id}",
                              "value": "${module/value}"},
                              </stl:inline>],
                           'version':
                           [<stl:inline stl:repeat="version product/versions">
                             {"id": "${version/id}",
                              "value": "${version/value}"},
                              </stl:inline>]}
                       ,</stl:inline>
                      }
  function update_tracker(){
      update_tracker_list('version');
      update_tracker_list('module');
  }
  </script>
<form id="form-table" action=";change_several_bugs?${search_parameters}" method="POST">
  ${batch} ${table}

  <br></br>
  <fieldset>
    <legend>Change Several Issues</legend>
<table>
  <tr>
    <td valign="top">
      <label for="product">Producto:</label><br></br>
      <select class="tracker-select" id="product" name="change_product">
        <option value="-1">Do not change</option>
        <option value="${item/id}" selected="${item/is_selected}" stl:repeat="item products">${item/title}</option>
      </select>
    </td>
    <td valign="top">
      <label for="module">Módulo:</label><br></br>
      <select class="tracker-select" id="module" name="change_module">
        <option value="-1">Do not change</option>
        <option value=""></option>
        <option value="${item/id}" selected="${item/is_selected}" stl:repeat="item modules">${item/title}</option>
      </select>
    </td>
    <td valign="top">
      <label for="version">Version:</label><br></br>
      <select class="tracker-select" id="version" name="change_version">
        <option value="-1">Do not change</option>
        <option value=""></option>
        <option value="${item/id}" selected="${item/is_selected}" stl:repeat="item versions">${item/title}</option>
      </select>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <label for="type">Tipo:</label><br></br>
      <select class="tracker-select" id="type" name="change_type">
        <option value="-1">Do not change</option>
        <option value="${item/id}" selected="${item/is_selected}" stl:repeat="item types">${item/title}</option>
      </select>
    </td>
    <td valign="top">
      <label for="state">Estado:</label><br></br>
      <select class="tracker-select" id="state" name="change_state">
        <option value="-1">Do not change</option>
        <option value="${item/id}" selected="${item/is_selected}" stl:repeat="item states">${item/title}</option>
      </select>
    </td>
    <td valign="top">
      <label for="priority">Prioridad:</label><br></br>
      <select class="tracker-select" id="priority" name="change_priority">
        <option value="-1">Do not change</option>
        <option value=""></option>
        <option value="${item/id}" selected="${item/is_selected}" stl:repeat="item priorities">${item/title}</option>
      </select>
    </td>
  </tr>
  <tr>
    <td colspan="3" valign="top">
      <label for="assigned-to">Asignar a:</label><br></br>
      <select class="tracker-select" id="assigned-to" name="change_assigned_to">
        <option value="do-not-change">Do not change</option>
        <option value=""></option>
        <option value="${item/name}" selected="${item/selected}" stl:repeat="item assigned_to">${item/value}</option>
      </select>
    </td>
  </tr>
  <tr>
    <td colspan="6">
      <label for="comment">Comentario:</label>
      <br></br>
      <textarea id="comment" rows="10" cols="68" name="comment"></textarea>
    </td>
  </tr>
  <tr>
    <td colspan="6">
      <button class="button-ok" type="submit">Edit Issues</button>
    </td>
  </tr>
</table>
  </fieldset>
</form>

</stl:block>
