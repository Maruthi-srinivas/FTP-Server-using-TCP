// //code for merge sort

// #include<stdio.h>
// #include<stdlib.h>

// int merge(int arr[],int low,int high){
//     int mid=(low+high)/2;
//     int a=mid-left+1;
//     int b=high-mid;
//     int l[a],r[b];
//     for(int i=0;i<a;i++){
//         l[i]=arr[high+i];
//     }
//     for(int j=0;j<b;j++){
//         r[j]=arr[mid+i+j];
//     }
//     int i=0;j=0;k=low;
//     while(i<a && j<b){
//         if(l[i]<=r[j]){
//             arr[k++]=l[i++];
//         }
//         else{
//             arr[k++]=r[j++];
//         }
//     }
// }
// void mergesort(int arr[],int low,int high){
//     if(low<high){
//         int mid=low+(high-low)/2;
//         mergesort(arr,low,mid);
//         mergesort(arr,mid+1,high);
//         mergesort(arr,low,mid,high);
        
//     }
// }



#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <limits.h>
#define PLACES 5

int minpathcost = INT_MAX;
int minpath[PLACES+1];
void copypath(int src[], int dest[], int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}
int calculatecost(int graph[][PLACES], int path[], int n) {
    int cost = 0;
    for (int i = 0; i < n - 1; i++) {
        cost += graph[path[i]][path[i + 1]];
    }
    cost += graph[path[n - 1]][path[0]];
    return cost;
}
void tsp(int graph[][PLACES], int path[], int visited[], int level, int n, int currentCost) {
    if (level == n) {
        int totalCost = currentCost + graph[path[level - 1]][path[0]];
        if (totalCost < minpathcost) {
            minpathcost = totalCost;
            copypath(path, minpath, n);
            minpath[n] = path[0];
        }
        return;
    }
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            visited[i] = 1;
            path[level] = i;
            int newcost = currentCost + graph[path[level - 1]][i];
            if (newcost < minpathcost) {
                tsp(graph, path, visited, level + 1, n, newcost);
            }
            visited[i] = 0;
        }
    }
}
int main() {
    int graph[PLACES][PLACES];
    int path[PLACES];
    int visited[PLACES] = {0};
    for (int i = 0; i < PLACES; i++) {
        for (int j = 0; j < PLACES; j++) {
            scanf("%d", &graph[i][j]);
        }
    }
    visited[0] = 1; // Start from city 0
    path[0] = 0;
    tsp(graph, path, visited, 1, PLACES, 0);
    printf("Shortest path: %d\nPath: ", minpathcost);
    for (int i = 0; i <= PLACES; i++) {
        printf("%d ", minpath[i]);
    }
    printf("\n");

    return 0;
}
