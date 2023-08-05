<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">

<form name="loginform" method="post" id="loginform" action=";login">
  <fieldset>
    <legend>Identificarse</legend>
    <dl>
      <dt>
        <label for="username" class="${username/class}">Dirección de correo electrónico</label>
      </dt>
      <dd>
        <input value="${username/value}" name="username" id="username" type="text"></input>
      </dd>
      <dt>
        <label for="password" class="${password/class}">Contraseña</label>
      </dt>
      <dd>
        <input id="password" name="password" type="password"></input>
        <a href="/;forgotten_password">Olvidé mi contraseña</a>
      </dd>
    </dl>
    <button class="button-ok" type="submit">Identificarse</button>
  </fieldset>

  <script language="javascript">
    <stl:inline stl:if="not username/value">$("#username").focus();</stl:inline>
    <stl:inline stl:if="username/value">$("#password").focus();</stl:inline>
  </script>
</form>

</stl:block>
