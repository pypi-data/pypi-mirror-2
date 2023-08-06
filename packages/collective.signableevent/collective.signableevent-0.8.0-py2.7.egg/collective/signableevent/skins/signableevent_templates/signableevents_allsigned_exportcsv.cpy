
csvdata = context.portal_signable_event.exportAllSignupCsv()
REQUEST = context.REQUEST
REQUEST.RESPONSE.setHeader('Content-type','text/csv')
REQUEST.RESPONSE.setHeader('Content-disposition','inline; filename="%s.csv"' % str(context.title_or_id()))
return csvdata
