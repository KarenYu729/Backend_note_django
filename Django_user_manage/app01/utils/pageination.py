import math
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy


class Pagination(object):
    """
    :param

    """
    def __init__(self, request, queryset, page_size=5, page_param="page"):
        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        query_dict = copy.deepcopy(request.GET)
        # allowed changes
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page = page
        self.page_param = page_param
        self.plus = int(page_size / 2)
        self.page_size = page_size

        self.start = (page-1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count = math.ceil(total_count / page_size)

        self.total_page = total_page_count
        print(type(self.plus))


    def html(self):
        if self.total_page <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            elif self.page <= self.total_page - self.plus:
                start_page = self.page - self.plus
                end_page = self.page + self.plus
            else:
                start_page = self.total_page - 2 * self.plus
                end_page = self.total_page
        self.start_page = start_page
        self.end_page = end_page

        self.query_dict.setlist(self.page_param, [1])

        page_str_list = []
        # add first page
        front = '<li><a href="?page={}">Front page</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(front)
        # add previous page
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">&laquo;</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">&laquo;</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(self.start_page, self.end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # add next page
        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">&raquo;</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page])
            prev = '<li><a href="?{}">&raquo;</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # add last page
        self.query_dict.setlist(self.page_param, [self.total_page])
        last = '<li><a href="?{}">End page</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last)

        page_str_list.append("""
        <li>
                    <form method="get">

                        <input type="text" name="page" class="form-control" placeholder="Page"
                               style="width: 100px; display:inline-block; float: left;">

                        <span class="input-group-btn">
                        <button type="submit" class="btn btn-default" style="border-radius: 5px">Turn to page</button>
                        </span>

                    </form>
                </li>
        """)

        page_string = mark_safe("".join(page_str_list))
        return page_string
