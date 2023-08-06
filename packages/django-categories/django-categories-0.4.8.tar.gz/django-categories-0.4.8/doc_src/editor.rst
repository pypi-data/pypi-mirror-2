
=======================
The Hierarchical Editor
=======================

Subclass your model's admin from  ``TreeEditor`` and ``admin.ModelAdmin``\ .

::

class SampleAdmin(TreeEditor, admin.ModelAdmin):
    pass

Always renders either the ``__unicode__`` or an attribute (function, property or field) named ``short_title``