from django.contrib import messages
from django.views.generic import (DeleteView,
                                  DetailView,
                                  ListView,
                                  TemplateView)

from extra_views import (CreateWithInlinesView,
                         InlineFormSet,
                         UpdateWithInlinesView)

from market.apps.board.forms import (ImageHelper,
                                     PostForm,
                                     PostUpdateForm)
from market.apps.board.models import (Post,
                                      PostImage)
from market.apps.core.mixins import (CreateWithOwnerMixin,
                                     OwnerRequiredMixin,
                                     SellerRequiredMixin)


class ImagesInline(InlineFormSet):
    model = PostImage
    fields = ['image']
    extra = 5
    max_num = 5
    # can_delete = False


class PostCreateView(CreateWithOwnerMixin, SellerRequiredMixin, CreateWithInlinesView):
    model = Post
    inlines = [ImagesInline]
    form_class = PostForm
    template_name = 'board/post_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_helper'] = ImageHelper()
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Posting successfully created!', extra_tags='fa fa-check')
        return self.object.get_absolute_url()


class PostDeleteView(OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_delete.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'


class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    paginate_by = 8


class PostUpdateView(OwnerRequiredMixin, UpdateWithInlinesView):
    model = Post
    inlines = [ImagesInline]
    form_class = PostUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Posting successfully updated!', extra_tags='fa fa-check')
        return self.object.get_absolute_url()
