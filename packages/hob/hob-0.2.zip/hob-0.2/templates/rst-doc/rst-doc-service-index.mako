${len(service_name) * "="}
${service_name}
${len(service_name) * "="}

:Generated:  hob rst-doc

The following versions are available for the ${service_name} service.

.. toctree::
   :maxdepth: 1

% for service in services:
   ${'.'.join(service.options["version"].value.split('.')[:2])} <${service_name}/${service_name}_${'_'.join(service.options["version"].value.split('.')[:2])}.rst>
% endfor
