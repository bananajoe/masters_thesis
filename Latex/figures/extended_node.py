from zss.simple_tree import Node

class ExtendedNode(Node):
    def get_list(self):
        #recursive function that returns a nested list representing the tree structure
        #used to create example trees

    def number_of_leaves(self):
        #returns the overall number of leaves in the tree

    def list_of_leaves(self):
        #returns a list of the leaf-nodes (objects) in the tree

    def list_of_leaf_labels(self):
        #returns a list of the labels (string) of the leaves in the tree

    def get_clusters(self, exclude_leaf_labels = 0):
        #returns a list of the clusters in this tree

    def label_leaves_randomly(self):
        #during construction of tree examples we first construct trees and afterwards label them randomly