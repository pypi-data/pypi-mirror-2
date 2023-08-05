<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">

<form id="form-table" action=";export_to_csv" method="GET">
  <stl:block stl:repeat="param search_parameters">${param}</stl:block>

  ${batch} ${table}
  <br></br>
  <fieldset>
    <legend>Exportar a CSV</legend>
    Please select encoding:<br></br><br></br>
    <input value="oo" type="radio" id="editor-oo" name="editor" checked="on"></input>
    <label for="editor-oo"> For OpenOffice (Encoding: UTF-8, Separator: ",") </label>  <br></br>  <input value="excel" type="radio" id="editor-excel" name="editor"></input>  <label for="editor-excel"> For Excel (Encoding: CP1252, Separator: ";") </label>  <br></br><br></br>  <button class="button-ok" type="submit">Export</button>
  </fieldset>
</form>

</stl:block>
