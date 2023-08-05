<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<stl:block xmlns="http://www.w3.org/1999/xhtml" xmlns:stl="http://www.hforge.org/xml-namespaces/stl">
  <form method="post" action="${action}" id="wiki-form">
    <fieldset>
      <legend>${title}</legend>
      <p class="field-required" stl:if="has_required_widget">${required_msg}</p>
      <dl>
        <stl:block stl:repeat="widget widgets">
          <dt class="${widget/class}">
            <label for="${widget/name}" class="${widget/class}"> ${widget/title} </label>  <span class="field-mandatory" stl:if="widget/mandatory">(mandatory)</span>  <span class="field-multiple" stl:if="widget/multiple">(multiple)</span>  <span class="field-format" stl:if="widget/tip">${widget/tip}</span>
          </dt>
          <dd>
            ${widget/widget} <span class="field-suffix" stl:if="widget/suffix">${widget/suffix}</span>
          </dd>
        </stl:block>
        <div class="mceEditor defaultSkin">
          <table class="mceLayout" cellpadding="0" id="data-table" cellspacing="0">
            <tbody>
              <tr class="mceFirst">
                <td class="mceToolbar mceLeft mceFirst mceLast">
                  <table class="mceToolbar mceToolbarRow1 Enabled" cellpadding="0" id="data-toolbar1" align="" cellspacing="0">
                    <tbody>
                      <tr>
                        <td class="mceToolbarStart mceToolbarStartButton mceFirst">
                          <span><!-- IE --></span>
                        </td>
                        <td>
                          <a id="data-bold" href="javascript:;" class="mceButton mceButtonEnabled mce_bold" title="Negrita" onclick="return wiki_bold();">
                            <span class="mceIcon mce_bold"></span>
                          </a>
                        </td>
                        <td>
                          <a id="data-italic" href="javascript:;" class="mceButton mceButtonEnabled mce_italic" title="Cursiva" onclick="return wiki_italic();">
                            <span class="mceIcon mce_italic"></span>
                          </a>
                        </td>
                        <td>
                          <span class="mceSeparator"></span>
                        </td>
                        <td>
                          <a id="data-bullist" href="javascript:;" class="mceButton mceButtonEnabled mce_bullist" title="Unordered list" onclick="return wiki_bullist();">
                            <span class="mceIcon mce_bullist"></span>
                          </a>
                        </td>
                        <td>
                          <a id="data-numlist" href="javascript:;" class="mceButton mceButtonEnabled mce_numlist" title="Ordered list" onclick="return wiki_numlist();">
                            <span class="mceIcon mce_numlist"></span>
                          </a>
                        </td>
                        <td>
                          <span class="mceSeparator"></span>
                        </td>
                        <td>
                          <a id="data-link" href="javascript:;" class="mceButton mce_link mceButtonEnabled" title="Insertar enlace" onclick="return wiki_link();">
                            <span class="mceIcon mce_link"></span>
                          </a>
                        </td>
                        <td>
                          <a id="data-image" href="javascript:;" class="mceButton mceButtonEnabled mce_image" title="Insertar imagen" onclick="return wiki_image();">
                            <span class="mceIcon mce_image"></span>
                          </a>
                        </td>
                        <td>
                          <span class="mceSeparator"></span>
                        </td>
                        <td>
                          <a id="data-table" href="javascript:;" class="mceButton mceButtonEnabled mce_table" title="Insertar tabla" onclick="return wiki_table();">
                            <span class="mceIcon mce_table"></span>
                          </a>
                        </td>
                        <td>
                          <span class="mceSeparator"></span>
                        </td>
                        <td>
                          <table id="data-formatselect" cellpadding="0" class="mceListBox mceListBoxEnabled mce_formatselect" cellspacing="0">
                            <tbody>
                              <tr>
                                <td class="mceFirst">
                                  <a id="data-formatselect-text" href="javascript:;" class="mceText" onclick="return wiki_format();">Formato</a>
                                </td>
                                <td class="mceLast">
                                  <a id="data-formatselect-open" href="javascript:;" class="mceOpen" tabindex="-1" onclick="return wiki_format();">
                                    <span><!-- IE --></span>
                                  </a>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                        <td>
                          <span class="mceSeparator"></span>
                        </td>
                        <td>
                          <a id="data-small" href="javascript:;" class="mceButton mceButtonEnabled" title="Small Edit Text" onclick="return text_small();">
                            <img src="/ui/wiki/text_small.png"></img>
                          </a>
                        </td>
                        <td>
                          <a id="data-medium" href="javascript:;" class="mceButton mceButtonEnabled" title="Medium Edit Text" onclick="return text_medium();">
                            <img src="/ui/wiki/text_medium.png"></img>
                          </a>
                        </td>
                        <td>
                          <a id="data-large" href="javascript:;" class="mceButton mceButtonEnabled" title="Large Edit Text" onclick="return text_large();">
                            <img src="/ui/wiki/text_large.png"></img>
                          </a>
                        </td>
                        <td>
                          <a id="data-help" href="javascript:;" class="mceButton mceButtonEnabled" title="Help" onclick="return wiki_help();">
                            <img src="/ui/wiki/help.png"></img>
                          </a>
                        </td>
                        <td class="mceToolbarEnd mceToolbarEndListBox mceLast">
                          <span><!-- IE --></span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
              <tr>
                <td class="mceIframeContainer mceFirst mceLast">
                  <div class="mceContentBody" id="tinymce" dir="ltr">
                    <textarea id="data" rows="19" wrap="physical" cols="80" name="data">${data}</textarea>
                  </div>
                </td>
              </tr>
              <tr class="mceLast">
                <td class="mceStatusbar mceFirst mceLast">
                  <a id="data-resize" href="javascript:;" class="mceResize"></a>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="mcePlaceHolder" id="mcePlaceHolder" style="width: 0px; height: 0px; display: none;"></div>
        </div>
      </dl>
      <p>
        <a name="bottom" id="bottom"></a>
        <button value="save" type="submit" class="button-ok" name="action">Save</button>  <button value="save_and_view" type="submit" class="button-ok" name="action">Save &amp; View</button>
      </p>
    </fieldset>
  </form>

  <!-- Format Select Dropdown Menu -->
  <div class="mceListBoxMenu mceNoIcons defaultSkin" id="data-formatselect-menu" style="position: absolute; left: 625px; top: 199px;
    z-index: 200000; display: none; width: 129px; height: 120px;">
    <div class="mceMenu mceListBoxMenu mceNoIcons defaultSkin" id="data-formatselect-menu-co" style="width: 129px; height: 120px;">
      <span class="mceMenuLine"></span>
      <table cellpadding="0" id="data-formatselect-menu-tbl" border="0" cellspacing="0">
        <tbody>
          <tr class="mceMenuItem mceMenuItemEnabled mceFirst" id="mce_0">
            <td class="mceMenuItemTitle">
              <a href="javascript:;">
                <span class="mceIcon"></span>  <span class="mceText" title="Formato">Formato</span>
              </a>
            </td>
          </tr>
          <tr class="mceMenuItem mceMenuItemEnabled" id="mce_1">
            <td class="mce_formatPreview mce_pre">
              <a onclick="return wiki_preformatted();" href="javascript:;">
                <span class="mceIcon"></span>  <span class="mceText" title="Preformatted">Preformatted</span>
              </a>
            </td>
          </tr>
          <tr class="mceMenuItem mceMenuItemEnabled" id="mce_2">
            <td class="mce_formatPreview mce_h1">
              <a onclick="return wiki_heading1();" href="javascript:;">
                <span class="mceIcon"></span>  <span class="mceText" title="Heading 1">Heading 1</span>
              </a>
            </td>
          </tr>
          <tr class="mceMenuItem mceMenuItemEnabled" id="mce_3">
            <td class="mce_formatPreview mce_h2">
              <a onclick="return wiki_heading2();" href="javascript:;">
                <span class="mceIcon"></span>  <span class="mceText" title="Heading 2">Heading 2</span>
              </a>
            </td>
          </tr>
          <tr class="mceMenuItem mceMenuItemEnabled" id="mce_4">
            <td class="mce_formatPreview mce_h3">
              <a onclick="return wiki_heading3();" href="javascript:;">
                <span class="mceIcon"></span>  <span class="mceText" title="Heading 3">Heading 3</span>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <script type="text/javascript">
    $(document).ready(function() {
      setup_size();
      setup_resize();
      $('#data').focus();
    });
  </script>
</stl:block>
