
class TableObject(object):

    def __init__(self, tablename, fields, pk = 'id'):
        self.tablename = tablename
        self.fields = fields
        self.pk = pk
        self.update_items = []
        self.insert_items = []

    def reset(self):
        self.update_items = []
        self.insert_items = []

    def add(self, values):
        if values.has_key(self.pk):
            self.update_items.append(values)
        else:
            self.insert_items.append(values)

    @property
    def itemCount(self):
        return len(self.update_items) + len(self.insert_items)

class ObjectNotRegistered(Exception): pass

class DelayedSqlExecutor(object):

    def __init__(self, cursor, item_limit = 1000, paramtoken = '%s'):
        self.cursor = cursor
        self.item_limit = item_limit
        self.paramtoken = paramtoken
        self.objects = {}

    def addObject(self, tablename, fields, pk = 'id'):
        self.objects[tablename] = TableObject(tablename, fields, pk)

    @property
    def totalItemCount(self):
        total_items = 0
        to = None
        for k,v in self.objects.items():
            total_items += v.itemCount
        return total_items

    def addItem(self, tablename, values):
        to = self.objects.get(tablename, None)
        if not to:
            raise ObjectNotRegistered(tablename)
        
        if self.totalItemCount >= self.item_limit:
            self.executeSql()

        to.add(values)            

    def executeSql(self):        
        for k,v in self.objects.items():
            if v.update_items:
                sql = ['update %s set' % k]
                m = []
                for fieldname in v.fields:
                    if fieldname == v.pk:
                        continue
                    m.append("%s = %s" % (fieldname, self.paramtoken))
                sql.append(',\n'.join(m))
                sql.append('where %s = %s' % (v.pk, self.paramtoken))
                fieldvalues = []
                for items in v.update_items:
                    m = []
                    for fieldname in v.fields:
                        if fieldname == v.pk:
                            continue
                        if items.has_key(fieldname):
                            m.append(items[fieldname])
                        else:
                            m.append('')
                    m.append(items.get(v.pk))
                    fieldvalues.append(m)
                self.cursor.executemany('\n'.join(sql), fieldvalues)

            if v.insert_items:
                sql = 'insert into %s (%s) values (%s)' % \
                      (v.tablename, ', '.join([f for f in v.fields if f != v.pk]), ', '.join([self.paramtoken for f in v.fields if f != v.pk]))                
                fieldvalues = []
                for items in v.insert_items:
                    m = []
                    for fieldname in v.fields:
                        if items.has_key(fieldname):
                            m.append(items[fieldname])
                    fieldvalues.append(m)
                self.cursor.executemany(sql, fieldvalues)
            v.reset()

    def close(self):
        self.executeSql()