<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">

  <!-- Edit Languages -->
  <fieldset>
    <legend>Edit the active languages</legend>
    <form id="browse-list" action="" method="post">
      <table summary="Configuration des langues">
        <thead>
          <tr>
            <th>Default</th>
            <th>Nombre</th>
            <th>Código</th>
          </tr>
        </thead>
        <tbody>
          <tr stl:repeat="language active_languages" class="${repeat/language/even}">
            <td stl:if="language/isdefault">Sí</td>
            <td stl:if="not language/isdefault">
              <input class="checkbox" value="${language/code}" name="codes" type="checkbox"></input>
            </td>
            <td>${language/name}</td>
            <td>${language/code}</td>
          </tr>
        </tbody>
      </table>
      <p>
        <button value="change_default_language" type="submit" class="button-ok" name="action">Change default</button>  <button value="remove_languages" type="submit" class="button-delete" name="action">Remove</button>
      </p>
    </form>
  </fieldset>

  <br></br>

  <!-- Add Language -->
  <fieldset>
    <legend>Agregar otro idioma</legend>
    <form action="" method="post">
      <select id="new-language" name="code">
        <option value="">Elije un idioma</option>
        <option value="${language/code}" stl:repeat="language not_active_languages">${language/name}</option>
      </select>
      <button value="add_language" type="submit" class="button-ok" name="action">Agregar</button>
    </form>
  </fieldset>

</stl:block>
