Introduction
============
Products.PFGSelectionStringField is a field type for Products.PloneFormGen.
It adds string field next to each selection options.

* For Mail adapter or what ever templates,use the following template code

::

  <html xmlns="http://www.w3.org/1999/xhtml">
  <head><title></title></head>
  <body>
    <p tal:content="here/body_pre | nothing" />
    <dl>
      <tal:block repeat="field options/wrappedFields">
        <dt tal:content="field/fgField/widget/label" />
        <tal:block tal:condition="not:python:field.fgField.getName()==request.form.get('ssf_id', None)">
          <dd tal:content="structure python:field.htmlValue(request)" />
        </tal:block>
        <tal:block tal:condition="python:request.form.get(field.fgField.getName(), None)">
          <tal:block tal:condition="python:field.fgField.getName()==request.form.get('ssf_id', None)">
            <dd>
              <tal:block tal:define="ssf_id python:request.form.get('ssf_id');
                                     ssf python:request.form.get(ssf_id);
                                     selected_field python:ssf_id+'_'+ssf;
                                     ssf_value python:request.form.get(selected_field)">
                <span tal:replace="ssf" />
                <br />
                <span tal:replace="ssf_value" />
              </tal:block>
            </dd>
          </tal:block>
        </tal:block>
      </tal:block>
    </dl>
    <p tal:content="here/body_post | nothing" />
    <pre tal:content="here/body_footer | nothing" />
  </body>
  </html>
