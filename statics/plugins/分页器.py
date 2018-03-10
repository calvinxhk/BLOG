class PageX:
    '''
    需要传入 数据列表，每页显示条数，当前页数，当前url
    :param data 数据列表，
    :param perpage 每页显示数量
    :param pageamount 前后页数
    :param page 当前页数
    :param url 当前页面url
    :return 数据列表，分页列表
    '''

    def __init__(self,data,url,perpage=10,page=1,pageamount=3):
        self.data = data
        self.pageamount = pageamount
        self.perpage = perpage
        if len(data)%perpage:
            self.max_page_number = len(data)//perpage+1
        else:
            self.max_page_number = len(data)//perpage
        try:
            self.page = int(page)
        except Exception:
            self.page = 1

        if self.page not in range(1,self.max_page_number+1):
            self.page = 1
        self.previous_page_number = self.page-1
        self.next_page_number = self.page+1
        self.url = url

    def has_previous(self):
        '''
        判断之前有无页数
        :return:
        '''
        if self.previous_page_number:
            return True
        else:return False

    def has_next(self):
        '''
        判断之后有无页数
        :return:
        '''
        if self.next_page_number <self.max_page_number:
            return True
        else:return False

    def object_list(self):
        '''
        每页数据
        :return: 数据列表
        '''
        start = self.previous_page_number*self.perpage
        end = self.page*self.perpage
        return self.data[start:end]

    def page_list(self):
        '''
        分页列表
        :return: a标签列表
        '''
        paginator=[]
        if self.has_previous():
            url = self.url + '?page='+str(self.previous_page_number)
        else:
            url = self.url + '?page=' + str(self.page)
        p = '<a  href="%s">上一页</a>'%url
        paginator.append(p)
        page_bgein= self.page-self.pageamount
        page_end = self.page+self.pageamount
        if page_bgein < 1:
            page_bgein = 1
        if page_end >= self.max_page_number:
            page_end = self.max_page_number
        for i in range(page_bgein,page_end+1):
            p = '<a href="'+self.url+'?page='+str(i)+'">'+str(i)+'</a>'
            paginator.append(p)
        if self.has_next():
            url = self.url + '?page='+str(self.next_page_number)
        else:
            url = self.url + '?page=' + str(self.page)
        p = '<a  href="%s">下一页</a>'%url
        paginator.append(p)
        return paginator



