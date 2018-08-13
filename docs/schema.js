var codec = new window.coreapi.codecs.CoreJSONCodec()
var coreJSON = window.atob('eyJfdHlwZSI6ImRvY3VtZW50IiwiX21ldGEiOnsidXJsIjoiaHR0cDovLzEyNy4wLjAuMTo4Njg2L2RvY3Mvc2NoZW1hLmpzIiwidGl0bGUiOiLnvo7lrrnlhbvnlJ8ifSwidXNlciI6eyJsaXN0Ijp7Il90eXBlIjoibGluayIsInVybCI6Ii9ob21lL3VzZXIvIiwiYWN0aW9uIjoiZ2V0IiwiZGVzY3JpcHRpb24iOiLliJflh7rmiYDmnInnmoTnlKjmiLfmiJbogIXliJvlu7rnlKjmiLciLCJmaWVsZHMiOlt7Im5hbWUiOiJwYWdlIiwibG9jYXRpb24iOiJxdWVyeSIsInNjaGVtYSI6eyJfdHlwZSI6ImludGVnZXIiLCJkZXNjcmlwdGlvbiI6IkEgcGFnZSBudW1iZXIgd2l0aGluIHRoZSBwYWdpbmF0ZWQgcmVzdWx0IHNldC4iLCJ0aXRsZSI6IlBhZ2UifX0seyJuYW1lIjoiaXRlbSIsImxvY2F0aW9uIjoicXVlcnkiLCJzY2hlbWEiOnsiX3R5cGUiOiJpbnRlZ2VyIiwiZGVzY3JpcHRpb24iOiJOdW1iZXIgb2YgcmVzdWx0cyB0byByZXR1cm4gcGVyIHBhZ2UuIiwidGl0bGUiOiJQYWdlIHNpemUifX1dfSwiY3JlYXRlIjp7Il90eXBlIjoibGluayIsInVybCI6Ii9ob21lL3VzZXIvIiwiYWN0aW9uIjoicG9zdCIsImVuY29kaW5nIjoiYXBwbGljYXRpb24vanNvbiIsImRlc2NyaXB0aW9uIjoi5YiX5Ye65omA5pyJ55qE55So5oi35oiW6ICF5Yib5bu655So5oi3IiwiZmllbGRzIjpbeyJuYW1lIjoidWlkIiwicmVxdWlyZWQiOnRydWUsImxvY2F0aW9uIjoiZm9ybSIsInNjaGVtYSI6eyJfdHlwZSI6InN0cmluZyIsImRlc2NyaXB0aW9uIjoiIiwidGl0bGUiOiJVaWQifX0seyJuYW1lIjoibW9iaWxlIiwicmVxdWlyZWQiOnRydWUsImxvY2F0aW9uIjoiZm9ybSIsInNjaGVtYSI6eyJfdHlwZSI6InN0cmluZyIsImRlc2NyaXB0aW9uIjoiIiwidGl0bGUiOiLnlKjmiLfmiYvmnLrlj7cifX0seyJuYW1lIjoidXNlcm5hbWUiLCJsb2NhdGlvbiI6ImZvcm0iLCJzY2hlbWEiOnsiX3R5cGUiOiJzdHJpbmciLCJkZXNjcmlwdGlvbiI6IiIsInRpdGxlIjoi55So5oi35ZCNIn19LHsibmFtZSI6ImlzX2ZyZWVfZXhwZXJpZW5jZSIsImxvY2F0aW9uIjoiZm9ybSIsInNjaGVtYSI6eyJfdHlwZSI6ImJvb2xlYW4iLCJkZXNjcmlwdGlvbiI6IiIsInRpdGxlIjoi5piv5ZCm5bey57uP5YWN6LS55L2T6aqM6L+H5LqG5byA5bqX5LyY5oOgIn19XX19LCJ1c2VycyI6eyJsaXN0Ijp7Il90eXBlIjoibGluayIsInVybCI6Ii9ob21lL3VzZXJzLyIsImFjdGlvbiI6ImdldCIsImRlc2NyaXB0aW9uIjoi5YiX5Ye65omA5pyJ55qE55So5oi35oiW6ICF5Yib5bu655So5oi3IiwiZmllbGRzIjpbeyJuYW1lIjoicGFnZSIsImxvY2F0aW9uIjoicXVlcnkiLCJzY2hlbWEiOnsiX3R5cGUiOiJpbnRlZ2VyIiwiZGVzY3JpcHRpb24iOiJBIHBhZ2UgbnVtYmVyIHdpdGhpbiB0aGUgcGFnaW5hdGVkIHJlc3VsdCBzZXQuIiwidGl0bGUiOiJQYWdlIn19LHsibmFtZSI6Iml0ZW0iLCJsb2NhdGlvbiI6InF1ZXJ5Iiwic2NoZW1hIjp7Il90eXBlIjoiaW50ZWdlciIsImRlc2NyaXB0aW9uIjoiTnVtYmVyIG9mIHJlc3VsdHMgdG8gcmV0dXJuIHBlciBwYWdlLiIsInRpdGxlIjoiUGFnZSBzaXplIn19XX0sImNyZWF0ZSI6eyJfdHlwZSI6ImxpbmsiLCJ1cmwiOiIvaG9tZS91c2Vycy8iLCJhY3Rpb24iOiJwb3N0IiwiZW5jb2RpbmciOiJhcHBsaWNhdGlvbi9qc29uIiwiZGVzY3JpcHRpb24iOiLliJflh7rmiYDmnInnmoTnlKjmiLfmiJbogIXliJvlu7rnlKjmiLciLCJmaWVsZHMiOlt7Im5hbWUiOiJ1aWQiLCJyZXF1aXJlZCI6dHJ1ZSwibG9jYXRpb24iOiJmb3JtIiwic2NoZW1hIjp7Il90eXBlIjoic3RyaW5nIiwiZGVzY3JpcHRpb24iOiIiLCJ0aXRsZSI6IlVpZCJ9fSx7Im5hbWUiOiJtb2JpbGUiLCJyZXF1aXJlZCI6dHJ1ZSwibG9jYXRpb24iOiJmb3JtIiwic2NoZW1hIjp7Il90eXBlIjoic3RyaW5nIiwiZGVzY3JpcHRpb24iOiIiLCJ0aXRsZSI6IueUqOaIt+aJi+acuuWPtyJ9fSx7Im5hbWUiOiJ1c2VybmFtZSIsImxvY2F0aW9uIjoiZm9ybSIsInNjaGVtYSI6eyJfdHlwZSI6InN0cmluZyIsImRlc2NyaXB0aW9uIjoiIiwidGl0bGUiOiLnlKjmiLflkI0ifX0seyJuYW1lIjoiaXNfZnJlZV9leHBlcmllbmNlIiwibG9jYXRpb24iOiJmb3JtIiwic2NoZW1hIjp7Il90eXBlIjoiYm9vbGVhbiIsImRlc2NyaXB0aW9uIjoiIiwidGl0bGUiOiLmmK/lkKblt7Lnu4/lhY3otLnkvZPpqozov4fkuoblvIDlupfkvJjmg6AifX1dfX19')
window.schema = codec.decode(coreJSON)