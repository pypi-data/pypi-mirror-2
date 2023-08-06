<%
  local_comments = comments or ["/** \n", " * ", " */"]
  span_close = classes and "</span>" or ""
  spans = {
      "comment": classes and "<span class=\"comment\">" or "",
      "message": classes and "<span class=\"message\">" or "",
      "number": classes and "<span class=\"number\">" or "",
      "bool": classes and "<span class=\"bool\">" or "",
      "string": classes and "<span class=\"string\">" or "",
      "bytes": classes and "<span class=\"bytes\">" or ""
    } 
  def get_maxs(message):   
    q, type, name, number = [], [], [], []
    for field in message.fields:
      q.append(len(field.q.name))
      type.append(len(field.typename()))
      name.append(len(field.name))
      number.append(len(str(field.number)))
    return {  
        'q': q and max(q) or 0, 
        'type': type and max(type) or 0, 
        'name': name and max(name) or 0, 
        'number': number and max(number) or 0
      }

  def get_submessages(fields, names=[]):
      ret = []
      for field in fields:
          if field.message and isinstance(field.message, proto.Message) and not field.message.name in names:
              names.append(field.message.name)
              ret.append(field)
              ret += get_submessages(field.message.fields, names)
      return ret
  submessages = get_submessages(message.fields)
%>\
  ## ************************************************************** ##
  ## def
  ## ************************************************************** ##
  ## print_doc
  ## ************************************************************** ##
<%def name="print_doc(doc, indent_level=0, indent='  ')">\
${(local_comments[0] and indent_level or 0)*indent}${spans['comment']}${local_comments[0]}\
      % for line in doc.text.splitlines():
${(indent_level)*indent}${local_comments[1]}${line.strip('\r\n')}
      % endfor
${(indent_level)*indent}${local_comments[2]}${span_close}\
</%def>\
  ## message_def
  ## ************************************************************** ##
<%def name="print_options(owner, options, indent_level=0, indent='  ')">\
<%
  opts = list(options.iteritems())
  olen = 0
  for option, value in opts:
    l = len(option)
    if owner.isCustomOption(option):
      l += 2
    olen = max(l, olen)
%>\
% for option, value in opts:
  % if value.doc:
${print_doc(value.doc, indent_level, indent)}
  % endif
  % if owner.isCustomOption(option):
${indent*indent_level}option ${("(%s)" % option).ljust(olen)} = ${value.dumps()};
  % else:
${indent*indent_level}option ${option.ljust(olen)} = ${value.dumps()};
  % endif
% endfor
</%def>\
\
<%def name="print_enum(enum, indent_level=0, indent='  ')">\
% if enum.doc:
${print_doc(enum.doc, indent_level, indent)}
% endif
${indent*indent_level}enum ${enum.name}
${indent*indent_level}{
% if enum.options:
${print_options(enum, enum.options, indent_level+1, indent)}
% endif
% for value in enum.values:
  % if value.doc:
${print_doc(value.doc, indent_level+1, indent)}
  % endif
${indent*(indent_level+1)}${value.name} = ${value.value};
% endfor
${indent*indent_level}}
</%def>\
\
<%def name="message_def(message, submessages=None, indent_level=0, indent='  ')">\
<% maxs = get_maxs(message) %>\
  % if message.doc:
${print_doc(message.doc, indent_level, indent)}
  % endif
  % if message.comment:
${indent_level*indent}${spans['comment']}// ${message.comment}${span_close}
  % endif
${indent_level*indent}message ${spans['message']}${message.name}${span_close}
${indent_level*indent}{
  % if submessages:
    % for submsg in submessages:
${message_def(submsg.message, submessages=None, indent_level=indent_level+1)}
    % endfor
  % endif
% if message.enums:
  % for enum in message.enums:
${print_enum(enum, indent_level+1, indent)}
  % endfor
% endif
% if message.options:
${print_options(message, message.options, indent_level+1, indent)}
% endif
  % for field in message.fields:
    % if field.doc:
${print_doc(field.doc, indent_level+1, indent)}
    % endif
    % if field.comment:
${(indent_level+1)*indent}${spans['comment'] + "// " + field.comment + span_close}
    % endif
${(indent_level+1)*indent}${field.q.name.ljust(maxs['q'])} \
${spans[protoHTMLClass(field)]}${field.typename().ljust(maxs['type'])}${span_close} \
${field.name.ljust(maxs['name'])} = \
${str(field.number).rjust(maxs['number'])}; 
  % endfor
${indent_level*indent}}\
</%def>\
  ## ************************************************************** ##
  ## template
  ## ************************************************************** ##
${message_def(message, submessages=submessages, indent_level=indent_level)}
