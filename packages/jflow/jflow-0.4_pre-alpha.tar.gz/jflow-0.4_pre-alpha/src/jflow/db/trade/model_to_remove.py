        
        
class PortfolioView(TimeStamp):
    '''
    A portfolio view.
    This object defines a portfolio view for a particular Fund
    '''
    fund         = models.ForeignKey(Fund, related_name = 'views')
    name         = models.CharField(max_length=32)
    default      = models.BooleanField(default = False)
    description  = models.TextField(blank = True, null = True)
    user         = models.ForeignKey(User, null = True)
    
    def __unicode__(self):
        return u'%s: %s (%s)' % (self.fund,self.name,self.user)
        #try:
        #    u = self.userportfolioview
        #    return u'%s: %s (%s)' % (self.fund,self.name,u.user)
        #except:
        #    return u'%s: %s' % (self.fund,self.name)
    
    class Meta:
        unique_together = ('fund','name','user')
        
    def save(self):
        default   = self.default
        if default:
            pviews = self.fund.views.all()
            for view in pviews:
                view.default = False
                view.save()
            self.default = True
        super(PortfolioView,self).save()
        
    def set_as_default(self, user):
        '''
        Set the view as default for user 'user'
        '''
        if user and user.is_authenticated():
            des = UserViewDefault.objects.filter(user = user,
                                                 view__fund = self.fund)
            if des:
                des = list(des)
                d = des.pop(0)
                d.view = self
                d.save()
                for d in des:
                    d.delete()
            else:
                d = UserViewDefault(user = user,
                                    view = self)
                d.save()
            return d
        else:
            return None
    
    def is_default(self, user):
        des = self.userviewdefault_set.filter(user = user)
        if des:
            return True
        else:
            return False        
    
    def addFolder(self, parent, code):
        name = code[:32]
        code = code[:22]
        if isinstance(parent,Portfolio) and parent.view == self:
            c = parent.children.filter(code = code)
            if not c:
                c = Portfolio(code   = code,
                              name   = name,
                              parent = parent,
                              view   = parent.view,
                              fund   = parent.fund)
                c.save()
                return c
        elif isinstance(parent,Fund) and parent.can_have_folders():
            c = Portfolio.objects.filter(code = code,
                                         view = self,
                                         fund = parent)
            if not c:
                c = Portfolio(code = code,
                              name = name,
                              view = self,
                              fund = parent)
                c.save()
                return c
        return None
    
    def rootfolders(self):
        return self.portfolio_set.filter()
        

class UserViewDefault(models.Model):
    user = models.ForeignKey(User)
    view = models.ForeignKey(PortfolioView, related_name = 'user_default')
    
    def __unicode__(self):
        return '%s - %s' % (self.view,self.user)
    
    class Meta:
        unique_together = ('user','view')


class PortfolioDisplay(models.Model):
    '''
    Model for a portfolio display configuration
    '''
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, null = True)
    fields = models.TextField(blank=True)
    
    objects = managers.PortfolioDisplayManager()
    
    #class Meta:
    #    order = ('name',)
        
    def fieldlist(self):
        return self.fields.replace(' ','').split(',')
        
    def todict(self):
        return {'name': self.name,
                'fields': self.fieldlist()}
