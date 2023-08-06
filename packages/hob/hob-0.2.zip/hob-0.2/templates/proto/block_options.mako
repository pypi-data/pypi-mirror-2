<%
  opts = list()
  olen = 0
  excludes = g.messageOptionExcludes
  for option, value in options.iteritems():
    if option in excludes:
      continue
    l = len(option)
    if owner.isCustomOption(option):
      l += 2
    olen = max(l, olen)
    opts.append((option, value))
%>\
% for option, value in opts:
  % if value.doc:
${value.doc.toComment()}
  % endif
  % if owner.isCustomOption(option):
option ${("(%s)" % option).ljust(olen)} = ${value.dumps()};
  % else:
option ${option.ljust(olen)} = ${value.dumps()};
  % endif
% endfor