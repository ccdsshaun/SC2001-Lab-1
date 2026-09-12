import math
import random
import time

def HybridMergeSort(A, start, end, S, key_comp):
    ## Switch to Insertion Sort if size <= S
    if end - start <= S:
        InsertionSort(A, start, end, key_comp) 
        return        ## A and key_comp are mutable
    else:
        mid = start + math.floor((end - start) / 2)
        HybridMergeSort(A, start, mid, S,key_comp)
        HybridMergeSort(A, mid, end, S,key_comp)
        Merge(A, start, mid, end, key_comp)
        return        ## A and key_comp are mutable

def InsertionSort(A, start, end, key_comp):
    for i in range(start + 1, end): 
        j = i - 1
        while j >= start:
            key_comp[0] += 1  # Comparison A[j] vs A[j+1] occurs here
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                j -= 1
            else:
                break  # Comparison evaluated to False; stop shifting

def MergeSort(A, start, end, key_comp):
    if end - start <= 1:
        return
    mid = start + math.floor((end-start)/2)

    MergeSort(A, start, mid, key_comp)
    MergeSort(A, mid, end, key_comp)

    Merge (A, start, mid, end, key_comp)

def Merge(A, start, mid, end, key_comp):
    i = 0
    k = start
    B_left = A[start:mid]
    B_right = A[mid:end]

    for j in range(0, len(B_right)):
        while i < len(B_left):
            key_comp[0] += 1  # Comparison B_left[i] vs B_right[j] occurs here
            if B_left[i] <= B_right[j]:
                A[k] = B_left[i]
                i += 1
                k += 1
            else:
                break  # Comparison evaluated to False; take B_right[j]
        A[k] = B_right[j]
        k += 1

    # Remaining elements in B_left do not require any key comparisons
    while i < len(B_left):
        A[k] = B_left[i]
        i += 1
        k += 1

def generate_array(n, x):
    # Generates an array of size n with random integers in range [1, x]
    return [random.randint(1, x) for i in range(n)]

def key_comparison (arr, S):
    key_comp = [0]
    HybridMergeSort (arr, 0, len(arr), S, key_comp)
    return key_comp[0]

def HybridTest(arr, S): # Investigate the performance of the hybrid sorting algorithm in terms of CPU time and the number of key comparisos
    A = arr.copy() # Make a copy of the array 
    key_comp = [0] # Initialize the comparison counter
    
    start = time.process_time() 
    HybridMergeSort(A, 0, len(A), S, key_comp)
    end = time.process_time()
    
    cpuTime = end - start # Calculate CPU time
    
    return key_comp[0], cpuTime

def MergeTest(arr): # Investigate the performance of Merge Sort in terms of CPU time and the number of key comparisos
    A = arr.copy() # Make a copy of the array 
    key_comp = [0] # Initialize the comparison counter
    
    start = time.process_time()
    MergeSort(A, 0, len(A), key_comp)
    end = time.process_time()
    
    cpuTime = end - start # Calculate CPU time
    
    return key_comp[0], cpuTime
    
# Example: generate array of size 10, 000, 000 with x = 1,000,000
arr = generate_array(10000000, 1000000)

# Optimal Value of S
S = 4

A = [2, 3, 4, 1]
comparison = key_comparison (A, S)
print(A)
print("comparison:", comparison)


print("Original version of Merge Sort")
mergeComparison, mergeTime = MergeTest(arr)
print(f"Number of key comparisons: {mergeComparison}")
print(f"CPU Time: {mergeTime} seconds")

print()

print("Hybrid Algorithm")
hybridComparison, hybridTime = HybridTest(arr, S)
print(f"Number of key comparisons: {hybridComparison}")
print(f"CPU Time: {hybridTime} seconds")

print()

# Comparing the peformance of the hybrid sorting algorithm and Merge Sort
print("Algorithm \t\t Key Comparisons \t CPU Time (in s)")
print(f"Original Merge Sort \t {mergeComparison} \t\t {mergeTime}")
print(f"Hybrid Merge Sort \t {hybridComparison} \t\t {hybridTime}")

