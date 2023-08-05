# -*- coding: utf-8 -*-
<tbody>
%for field in fieldset.render_fields.itervalues():
  <tr>
    <td class="field_readonly">
      <label>
        ${[field.label_text, fieldset.prettify(field.key)][int(field.label_text is None)]|h}:
      </label>
      </td>
    <td>${field.render_readonly()|n}</td>
  </tr>
%endfor
</tbody>
