Integration with web frameworks
===============================
If we have a Django view::

  urls = (
    url(r'/api/search/(.*)', perform_search_view),
  )

  def perform_search_view(request):
      """Search API interface.
      """
      pass

We could do::
