## -*- coding: utf-8 -*-
## Copyright (C) 2007 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from types import StringType
from Products.CMFPlone.browser.navtree import NavtreeStrategyBase

from Products.CMFPlone.utils import base_hasattr

def buildFolderTree(context, obj=None, query={}, strategy=NavtreeStrategyBase()):
    """Create a tree structure representing a navigation tree. By default,
    it will create a full "sitemap" tree, rooted at the portal, ordered
    by explicit folder order. If the 'query' parameter contains a 'path'
    key, this can be used to override this. To create a navtree rooted
    at the portal root, set query['path'] to:

        {'query' : '/'.join(context.getPhysicalPath()),
         'navtree' : 1}

    to start this 1 level below the portal root, set query['path'] to:

        {'query' : '/'.join(obj.getPhysicalPath()),
         'navtree' : 1,
         'navtree_start' : 1}

    to create a sitemap with depth limit 3, rooted in the portal:

        {'query' : '/'.join(obj.getPhysicalPath()),
         'depth' : 3}

    The parameters:

    - 'context' is the acquisition context, from which tools will be acquired
    - 'obj' is the current object being displayed.
    - 'query' is a catalog query to apply to find nodes in the tree.
    - 'strategy' is an object that can affect how the generation works. It
        should be derived from NavtreeStrategyBase, if given, and contain:

            rootPath -- a string property; the physical path to the root node.

            If not given, it will default to any path set in the query, or the
            portal root. Note that in a navtree query, the root path will
            default to the portal only, possibly adjusted for any navtree_start
            set. If rootPath points to something not returned by the query by
            the query, a dummy node containing only an empty 'children' list
            will be returned.

            showAllParents -- a boolean property; if true and obj is given,
                ensure that all parents of the object, including any that would
                normally be filtered out are included in the tree.

            nodeFilter(node) -- a method returning a boolean; if this returns
                False, the given node will not be inserted in the tree

            subtreeFilter(node) -- a method returning a boolean; if this returns
                False, the given (folderish) node will not be expanded (its
                children will be pruned off)

            decoratorFactory(node) -- a method returning a dict; this can inject
                additional keys in a node being inserted.

    Returns tree where each node is represented by a dict:

        item            -   A catalog brain of this item
        depth           -   The depth of this item, relative to the startAt level
        currentItem     -   True if this is the current item
        currentParent   -   True if this is a direct parent of the current item
        children        -   A list of children nodes of this node

    Note: Any 'decoratorFactory' specified may modify this list, but
    the 'children' property is guaranteed to be there.

    Note: If the query does not return the root node itself, the root
    element of the tree may contain *only* the 'children' list.

    Note: Folder default-pages are not included in the returned result.
    If the 'obj' passed in is a default-page, its parent folder will be
    used for the purposes of selecting the 'currentItem'.
    """
    portal_url = getToolByName(context, 'portal_url')
    portal_catalog = getToolByName(context, 'portal_catalog')
    portal_languages = getToolByName(context, 'portal_languages')

    showAllParents = strategy.showAllParents
    rootPath = strategy.rootPath

    request = getattr(context, 'REQUEST', {})

    # Find the object's path. Use parent folder if context is a default-page

    objPath = None
    if obj is not None:
        if utils.isDefaultPage(obj, request):
            objPath = '/'.join(obj.getPhysicalPath()[:-1])
        else:
            objPath = '/'.join(obj.getPhysicalPath())

    portalPath = portal_url.getPortalPath()

    #replace path by getCanonicalPath
    if 'path' in query:
        query['getCanonicalPath'] = query['path']
        del query['path']

    # Calculate rootPath from the path query if not set.
    if 'getCanonicalPath' not in query:
        if rootPath is None:
            rootPath = portalPath
        query['getCanonicalPath'] = rootPath
    elif rootPath is None:
        pathQuery = query['getCanonicalPath']
        if type(pathQuery) == StringType:
            rootPath = pathQuery

        else:
            # Adjust for the fact that in a 'navtree' query, the actual path
            # is the path of the current context
            if pathQuery.get('navtree', False):
                navtreeLevel = pathQuery.get('navtree_start', 1)
                if navtreeLevel > 1:
                    navtreeContextPath = pathQuery['query']
                    navtreeContextPathElements = navtreeContextPath[len(portalPath)+1:].split('/')
                    # Short-circuit if we won't be able to find this path
                    if len(navtreeContextPathElements) < (navtreeLevel - 1):
                        return {'children' : []}
                    rootPath = portalPath + '/' + '/'.join(navtreeContextPathElements[:navtreeLevel-1])
                else:
                    rootPath = portalPath
            else:
                rootPath = pathQuery['query']

    rootDepth = len(rootPath.split('/'))

    # Default sorting and threatment of default-pages
    if 'sort_on' not in query:
        query['sort_on'] = 'getObjPositionInParent'

    if 'is_default_page' not in query:
        query['is_default_page'] = False

    #if the object has a getCanonicalPath method query this one
    if base_hasattr(obj, 'getCanonicalPath'):
        query['getCanonicalPath']['query'] = '/'.join(obj.getCanonicalPath())

#    #modify the navtree_start of the query so that there is no problem with translated roots
#    if query.get('navtree_start', 0) > 0:
#        query['navtree_start'] -= 1


    results = portal_catalog.searchResults(query)

    canonical = None
    if base_hasattr(obj, 'getCanonicalPath'):
        canonical = '/'.join(obj.getCanonicalPath())
    # We keep track of a dict of item path -> node, so that we can easily
    # find parents and attach children. If a child appears before its
    # parent, we stub the parent node.

    # This is necessary because whilst the sort_on parameter will ensure
    # that the objects in a folder are returned in the right order relative
    # to each other, we don't know the relative order of objects from
    # different folders. So, if /foo comes before /bar, and /foo/a comes
    # before /foo/b, we may get a list like (/bar/x, /foo/a, /foo/b, /foo,
    # /bar,).

    itemPaths = {}

    def insertElement(itemPaths, item, results, forceInsert=False):
        """Insert the given 'item' brain into the tree, which is kept in
        'itemPaths'. If 'forceInsert' is True, ignore node- and subtree-
        filters, otherwise any node- or subtree-filter set will be allowed to
        block the insertion of a node.
        """
        itemPath = item.getPath()
        itemCanonicalPath = '/'.join(item.getCanonicalPath)
        itemInserted = (itemPaths.get(itemPath, {}).get('item', None) is not None)

        # Short-circuit if we already added this item. Don't short-circuit
        # if we're forcing the insert, because we may have inserted but
        # later pruned off the node
        if not forceInsert and itemInserted:
            return

        itemPhysicalPath = itemPath.split('/')
        parentPath = '/'.join(itemPhysicalPath[:-1])
        itemCanonicalPhysicalPath = itemCanonicalPath.split('/')
        parentCanonicalPath = '/'.join(itemCanonicalPhysicalPath[:-1])

        parentPruned = False
        if len(itemPhysicalPath) - 1 == len(rootPath.split('/')):
            parentPath = rootPath
            parentPruned = (itemPaths.get(parentPath, {}).get('_pruneSubtree', False))
        else:
            for brain in results:
                if '/'.join(brain.getCanonicalPath) == parentCanonicalPath:
                    parentPath = brain.getPath()
                    parentPruned = (itemPaths.get(brain.getPath(), {}).get('_pruneSubtree', False))
                    break

        # Short-circuit if we know we're pruning this item's parent

        # XXX: We could do this recursively, in case of parent of the
        # parent was being pruned, but this may not be a great trade-off

        # There is scope for more efficiency improvement here: If we knew we
        # were going to prune the subtree, we would short-circuit here each time.
        # In order to know that, we'd have to make sure we inserted each parent
        # before its children, by sorting the catalog result set (probably
        # manually) to get a breadth-first search.

        if not forceInsert and parentPruned:
            return

        isCurrent = isCurrentParent = False
        if objPath is not None:
            if objPath == itemPath:
                isCurrent = True
            elif objPath.startswith(itemPath):
                isCurrentParent = True

        relativeDepth = len(itemPhysicalPath) - rootDepth

        newNode = {'item'          : item,
                   'depth'         : relativeDepth,
                   'currentItem'   : isCurrent,
                   'currentParent' : isCurrentParent}


        insert = True
        if not forceInsert and strategy is not None:
            insert = strategy.nodeFilter(newNode)
        if insert:

            if strategy is not None:
                newNode = strategy.decoratorFactory(newNode)

            # Tell parent about this item, unless an earlier subtree filter
            # told us not to. If we're forcing the insert, ignore the
            # pruning, but avoid inserting the node twice
            if itemPaths.has_key(parentPath):
                itemParent = itemPaths[parentPath]
                if forceInsert:
                    nodeAlreadyInserted = False
                    for i in itemParent['children']:
                        if i['item'].getPath() == itemPath:
                            nodeAlreadyInserted = True
                            break
                    if not nodeAlreadyInserted:
                        itemParent['children'].append(newNode)
                elif not itemParent.get('_pruneSubtree', False):
                    itemParent['children'].append(newNode)
            else:
                itemPaths[parentPath] = {'children': [newNode]}

            # Ask the subtree filter (if any), if we should be expanding this node
            if strategy.showAllParents and isCurrentParent:
                # If we will be expanding this later, we can't prune off children now
                expand = True
            else:
                expand = getattr(item, 'is_folderish', True)
            if expand and (not forceInsert and strategy is not None):
                expand = strategy.subtreeFilter(newNode)

            if expand:
                # If we had some orphaned children for this node, attach
                # them
                if itemPaths.has_key(itemPath):
                    newNode['children'] = itemPaths[itemPath]['children']
                else:
                    newNode['children'] = []
            else:
                newNode['children'] = []
                newNode['_pruneSubtree'] = True

            itemPaths[itemPath] = newNode

    # Add the results of running the query
    for r in results:
        insertElement(itemPaths, r, results)

#    def format(dic):
#        if type(dic) == type({}):
#            output = dic.copy()
#            for key in output.keys():
#                if key not in ['children','Title']:
#                    if type(output[key]) != type({}):
#                        del output[key]
#                    else:
#                        output[key] = format(output[key])
#                if key =='children':
#                    children = list(tuple(output.get('children',[])))
#                    output['children'] = children
#                    for i in range(len(children)):
#                        children[i] = format(children[i])
#            return output
#
#
#    print [brain.id for brain in results]
#    print format(itemPaths.get(rootPath, {'children' : []}))
#    print format(itemPaths)

    # Return the tree starting at rootPath as the root node. If the
    # root path does not exist, we return a dummy parent node with no children.
    return itemPaths.get(rootPath, {'children' : []})
