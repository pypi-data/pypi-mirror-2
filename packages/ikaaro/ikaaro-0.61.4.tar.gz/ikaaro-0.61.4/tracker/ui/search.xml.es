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
  <!-- Advanced Search -->
  <fieldset>
    <legend>Buscar<stl:block stl:if="search_name">: ${search_title}</stl:block>
    </legend>
    <form action=";view" method="get">
      <table>
        <tr>
          <td colspan="2">
            <label for="text">Text (search within the title and all comments) </label>  <br></br>
            <input name="text" size="30" id="text" class="tracker-select" type="text" value="${text}"></input>
          </td>
          <td colspan="1">
            <label for="mtime">Modified since:</label><br></br>
            <input value="${mtime}" type="text" id="mtime" size="2" name="mtime"></input> days ago
          </td>
        </tr>
        <tr>
          <td valign="top">
            <label for="product">Producto: (<a href="./product/;view">more ...</a>)</label>
            <br></br>
            <select class="tracker-select" id="product" name="product" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item products">${item/value}</option>
            </select>
          </td>
          <td valign="top">
            <label for="module">Módulo: (<a href="./module/;view">more ...</a>)</label>
            <br></br>
            <select class="tracker-select" id="module" name="module" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item modules">${item/value}</option>
            </select>
          </td>
          <td valign="top">
            <label for="version">Version: (<a href="./version/;view">more ...</a>)</label>
            <br></br>
            <select class="tracker-select" id="version" name="version" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item versions">${item/value}</option>
            </select>
          </td>
        </tr>
        <tr>
          <td valign="top">
            <label for="type">Tipo: (<a href="./type/;view">more ...</a>)</label>
            <br></br>
            <select class="tracker-select" id="type" name="type" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item types">${item/value}</option>
            </select>
          </td>
          <td valign="top">
            <label for="state">Estado: (<a href="./state/;view">more ...</a>)</label>
            <br></br>
            <select class="tracker-select" id="state" name="state" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item states">${item/value}</option>
            </select>
          </td>
          <td valign="top">
            <label for="priority">Prioridad: (<a href="./priority/;view">more ...</a>)</label>
            <br></br>
            <select class="tracker-select" id="priority" name="priority" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item priorities">${item/value}</option>
            </select>
          </td>
        </tr>
        <tr>
          <td colspan="3" valign="top">
            <label for="assigned-to">Assigned To:<stl:inline stl:if="is_admin"> (<a href="${manage_assigned}">edit</a>)</stl:inline></label>
            <br></br>
            <select class="tracker-select" id="assigned-to" name="assigned_to" size="4" multiple="multiple">
              <option value="${item/name}" selected="${item/selected}" stl:repeat="item assigned_to">${item/value}</option>
            </select>
          </td>
        </tr>
      </table>
      <br></br>
      <button value="view" type="submit" class="button-search" name="action">Search</button>
    </form>
  </fieldset>

</stl:block>
