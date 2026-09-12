import time
from part_a import HybridMergeSort, Merge, generate_array

def MergeSort(A, start, end):
    if end - start <= 1:
        return 0

    mid = start + (end - start) // 2

    left = MergeSort(A, start, mid)
    right = MergeSort(A, mid, end)
    mergeC = Merge(A, start, mid, end)

    return left + right + mergeC

def MergeTest(arr): # Investigate the performance of Merge Sort in terms of CPU time and the number of key comparisons
    A = arr.copy() # Make a copy of the array 
    
    start = time.process_time()
    key_comp = MergeSort(A, 0, len(A))
    end = time.process_time()
    
    cpuTime = end - start # Calculate CPU time
    
    return key_comp, cpuTime

def HybridTest(arr, S): # Investigate the performance of the hybrid sorting algorithm in terms of CPU time and the number of key comparisons
    A = arr.copy() # Make a copy of the array 

    start = time.process_time() 
    key_comp = HybridMergeSort(A, 0, len(A), S)
    end = time.process_time()
    
    cpuTime = end - start # Calculate CPU time
    
    return key_comp, cpuTime


arr = generate_array(10000000, 1000000) # Generate dataset of 10 million integers

S = 8

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
