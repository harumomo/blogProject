"""
自定义分页组件
       :param request: 页面请求
       :param queryset: 数据库查询语句
       :param page_size: 每页显示多少条数据，默认10条
       :param page_param: 页面传参，默认page
       :param plus: 当前页的前后显示多少页

使用方法：
    1.实例化此类,并传参
    page = Pagination(request,queryset)
    2.接收拆分好的数据
    queryset = page.page_queryset
    3.接收前端显示分页
    page_string = page.html()

    前端页面：
        <div class="container">
            <ul class="pagination">
                {{ page_string }}
            </ul>
        </div>
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        # page当前页，默认第一页
        page = request.GET.get(page_param, "1")
        # 传参不是整数类型转整数类型
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        # 拆分数据表起始和结束条数，如第1-10条，第11-20条
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据库总条数
        count = queryset.count()
        # 总页码total_page 向上取整
        total_page, div = divmod(count, page_size)
        if div:
            total_page += 1
        self.total_page = total_page
        self.plus = plus

    def html(self):
        # 计算出显示当前页的前五、后五页
        if self.total_page <= 2 * self.plus + 1:
            # 数据较少的情况
            start_page = 1
            end_page = self.total_page + 1
        else:
            # 极小值处理
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1 + 1
            else:
                # 极大值处理
                if (self.page + self.plus) > self.total_page:
                    start_page = self.page - self.plus
                    end_page = self.total_page + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1 + 1

        # 分页
        page_str_list = []

        # 首页
        page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))

        # 上一页
        if self.page > 1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)

        # 页码
        for i in range(start_page, end_page):
            if i == self.page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.page + 1)
        else:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.total_page)
        page_str_list.append(prev)

        # 尾页
        page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.total_page))

        page_string = mark_safe("".join(page_str_list))
        return page_string