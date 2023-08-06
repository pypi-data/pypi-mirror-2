<%
    service = package.services[0]
    title = service.name + " " + '.'.join(service.options["version"].value.split('.')[:2])
    is_draft = "draft" in service.options and service.options["draft"].value
%>\
${len(title) * "="}
${title}
${len(title) * "="}

:Generated:  hob rst-doc
:Version:    ${service.options["version"].value}
% if is_draft:
:Status:     Draft
% else:
:Status:     Published
% endif

${g.service(service)}

${g.commands(service)}
