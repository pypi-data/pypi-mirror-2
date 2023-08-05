class PagedCollection(object):
    """A class representing a page of search results."""

    def __init__(self, query, collection, klass):
        self.current_page_number = collection["current_page_number"]
        self.items = [klass(item) for item in self.__extract_as_array(collection, klass.__name__.lower())]
        self.klass = klass
        self.page_size = collection["page_size"]
        self.query = query
        self.total_items = collection["total_items"]

    def next_page(self):
        """
        Returns another :class:`PagedCollection <braintree.paged_collection.PagedCollection>` representing the
        next page of results or None if this is the last page.
        """

        if self.is_last_page:
            return None
        return self.klass.search(self.query, self.current_page_number + 1)

    @property
    def current_page_size(self):
        """Returns the number of items on this page."""

        if self.is_last_page:
            return self.total_items % self.page_size
        else:
            return self.page_size

    @property
    def is_last_page(self):
        """Returns whether this is the last page of results."""

        return self.total_items == 0 or self.current_page_number == self.total_pages

    @property
    def total_pages(self):
        """Returns the total number of pages of search results."""

        total_pages = self.total_items / self.page_size
        if self.total_items % self.page_size != 0:
            total_pages += 1
        return total_pages

    def __extract_as_array(self, collection, attribute):
        if not attribute in collection:
            return []

        value = collection[attribute]
        if type(value) != list:
            value = [value]
        return value

    def __getitem__(self, index):
        return self.items[index]
