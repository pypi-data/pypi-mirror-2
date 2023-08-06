========
Arboreal
========

Arboreal is a tool which lets you manage multiple trees. These trees are 
stored within the portal. They can be used in Archetypes as a vocabulary for
fields.


Installation
============

The tool comes with a GenericSetup profile. Therefore you can just install it
by going to the portal setup system. It will create a configlet which you can 
access via the same portal setup.

Integration with Archetypes
===========================

The primary usage for Arboreal is to use it for hierarchical vocabularies. To
make this a reality Arboreal has its own widget and field types.

An example of configuring a field within a schema is given below.

::

    MultiArborealField('groups',
        tree='tree_group_id',
        storeCompletePath = True,
        widget=MultiTreeSelectionWidget(
            label='Group',
            label_msgid='label_group',
            description_msgid='help_group',
            i18n_domain='JUNG',
        )
    ),


The tree is used as a vocabulary. You do not have to create this tree.
Arboreal will create it automatically when it does not exist. The
MultiTreeSelectionWidget is basically a multi selection widget which indents
the tree nodes using spaces. This gives the visual appearance of a tree. And
lastly we have the MultiArborealField. With this field you can get a list of
all paths stored. The storeCompletePath keyword toggles parent storage. It is
set to False by default. Parent storage works as follows.

Say you have a tree like given below:

- Node
  - Subnode
  
If you select the sub node in the interface and store it the path will be
stored. When storeCompletePath is set to False it will only contain the path
to Subnode. If storeCompletePath is set to True the parent will be stored as
well. An example of the differences:

storeCompletePath = False
-------------------------

path = [Node/Subnode]

storeCompletePath = True
-------------------------

path = [Node/Subnode, Node]

Storing the full path is useful for when you want to use the path as a
filtering mechanism. You can then easily do a catalog query on a keyword index
for a specific path. The reason we are not just using a path index is that you
can select multiple points in the tree.


Credits
========

Martijn Pieters (mj@jarn.com)
Jan Murre (jan.murre@pareto.nl)
Jeroen Vloothuis (jeroen.vloothuis@pareto.nl)

