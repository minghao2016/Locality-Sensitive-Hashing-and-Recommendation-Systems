# Locality-Sensitive-Hashing-and-Recommendation-Systems
This project will consider making movie recommendation and use LSH to efficiently find similar users for recommendation.

Part I: Finding similar users </br></br>
Suppose there are 100 different movies, numbered from 0 to 99. </br>
A user is represented as a set of movies. Jaccard coefficient is used to measure the similarity of sets. </br>
Apply minhash to obtain a signature of 20 values for each user. Recall that this is done by permuting the rows of characteristic matrix of movie-user matrix (i.e., row are movies and columns represent users). </br>
Assume that the i-th hash function for the signature: h(x,i) = (3x + i) % 100 (i = 1...20), where x is the original row number in the matrix. </br>
Apply LSH to speed up the process of finding similar users, where the signature is divided into 5 bands, with 4 values in each band. </br></br>

Part II: Making recommendations </br></br>
Based on the LSH result, for each user U, find top-5 users who are most similar to U (by their Jaccard similarity), and recommend movies that have been watched by at least 3 of these users (but not by U yet) to U.
