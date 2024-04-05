#include<stdio.h>
#include<stdlib.h>
struct node{
    int data;
    struct node *left;
    struct node *right;
};
int max(int a,int b){
    if(a>b){
        return a;
    }
    else{
        return b;
    }
}
struct node *newnode(int data){
    struct node *node=(struct node *)malloc(sizeof(struct node));
    node->data=data;
    node->left=NULL;
    node->right=NULL;
    return node;
}
int heightoftree(struct node *root){
    if(root==NULL){
        return -1;
    }
    else{
        return (max(heightoftree(root->left),heightoftree(root->right))+1);
    }
}

struct node *createtree(){
    struct node *root=newnode(1);
    root->left=newnode(2);
    root->right=newnode(3);
    root->left->left=newnode(4);
    root->left->right=newnode(5);
    root->right->left=newnode(6);
    root->right->right=newnode(7);
    root->left->left->left=newnode(8);
    return root;
}
int main(){
    struct node *root1=createtree();
    printf("Height of the tree root1 is %d",heightoftree(root1));
    return 0;
}