<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">

<form action=";new_resource?type=${class_id}" method="post">
  <fieldset>
    <legend>Add ${class_title}</legend>
    <dl>
      <dt><label for="title">Title</label></dt>
      <dd>
        <input id="title" name="title" size="40" type="text"></input>
      </dd>
      <dt><label for="name">Nombre</label></dt>
      <dd>
        <input id="name" name="name" size="40" type="text"></input>
      </dd>
      <stl:block stl:if="items">
        <dt>Choose the ${class_title} type</dt>
        <dd>
          <div stl:repeat="item items">
            <input value="${item/class_id}" type="radio" name="class_id" id="${item/class_id}" checked="${item/selected}"></input>
            <img src="${item/icon}" border="0"></img>  <label for="${item/class_id}">${item/title}</label>
          </div>
        </dd>
      </stl:block>
      <dt><label for="vhosts">Vhosts</label></dt>
      <dd>
        <p>Type the hostnames this website will apply to, each one in a different line.</p>
        <textarea name="vhosts" rows="7" cols="62">${vhosts}</textarea>
      </dd>
    </dl>
    <button class="button-ok" type="submit">Agregar</button>
  </fieldset>
</form>

<script type="text/javascript">
  $("#title").focus();
</script>

</stl:block>
