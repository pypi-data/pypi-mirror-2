<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">

<div class="context-menu">
  <label>${title}</label>
  <form action=";remember_search" method="post" style="margin: 4px 0px 0px 5px;">
    <input value="${search_name}" type="hidden" name="search_name" stl:if="search_name"></input>
    <input value="${item/value}" stl:repeat="item search_fields" name="${item/name}" type="hidden"></input>  <input value="${search_title}" name="search_title" style="width: 73%" size="18" type="text"></input>  <button class="button-ok" type="submit">Aceptar</button>
  </form>

  <form action=";forget_search" method="post" stl:if="search_name">
    <input value="${search_name}" name="search_name" type="hidden"></input>
    <button onclick="return confirm('Are you sure you want to forget this search?');" class="button-delete" type="submit">Olvidar esta Búsqueda</button>
  </form>
</div>

</stl:block>
