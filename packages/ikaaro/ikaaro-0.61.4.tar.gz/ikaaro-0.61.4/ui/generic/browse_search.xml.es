<?xml version="1.0" encoding="UTF-8"?>
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">

<form action="" method="get" stl:if="search_fields">
  <fieldset>
    <legend>Buscar</legend>
    <!-- Field -->
    <select name="search_field">
      <option value="${field/name}" selected="${field/selected}" stl:repeat="field search_fields">${field/title}</option>
    </select>
    <!-- Term -->
    <input value="${search_term}" name="search_term" size="35" type="text"></input>
    <!-- OK -->  <button class="button-search" type="submit">Aceptar</button>
  </fieldset>
</form>

</stl:block>
