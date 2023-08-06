<%
  commands = [command for command in service.itercommands()]
  commands.sort(key=lambda command: command.name)
  events = [command for command in service.iterevents()]
  events.sort(key=lambda event: event.name)
%>
% if commands:
Commands
========
  % for command in commands:
<%
  existing = {}
  references = list(command.message.references(existing))
  if command.response:
    references += list(command.response.references(existing))
%>\

.. index:: ${command.name}

``${command.name}``
${( 4 + len(command.name) ) * '-'}

::

  command ${command.name}(${command.messageName()}) returns (${command.responseName()}) = ${command.id};

  % if command.doc:
${command.doc.text}
  % endif

% if not command.message.name == "Default":
argument:

.. index:: ${command.message.name}

.. code-block:: c

${g.proto(level=2).message(command.message, indent=2)}
% endif

% if not command.response.name == "Default":
returns:

.. index:: ${command.response.name}

.. code-block:: c

${g.proto(level=2).message(command.response, indent=2)}
% endif

% if references:
references:

%   for message in references:
%     if not message.name == "Default":
.. index:: ${message.name}
%     endif:

.. code-block:: c

${g.proto(level=2).message(message, indent=2)}

%   endfor
% endif

  % endfor
% endif

% if events:
Events
======
  % for event in events:
<%
  existing = {}
  references = list(event.message.references(existing))
%>\

.. index:: ${event.name}

``${event.name}``
${( 4 + len(event.name) ) * '-'}

::

  event ${event.name} returns (${event.messageName()}) = ${event.id};

  % if event.doc:
${event.doc.text}
  % endif

message:

% if not command.message.name == "Default":
.. index:: ${command.message.name}
% endif

.. code-block:: c

${g.proto(level=2).message(event.message, indent=2)}

% if references:
references:

%   for message in references:
%     if not message.name == "Default":
.. index:: ${message.name}
%     endif

.. code-block:: c

${g.proto(level=2).message(message, indent=2)}

%   endfor
% endif

  % endfor
% endif
