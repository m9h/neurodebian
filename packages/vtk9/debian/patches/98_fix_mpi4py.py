Description: Fix mpi4py search
Author: Anton Gladky <gladk@debian.org>
Last-Update: 2021-09-17

Index: VTK-9.3.0/Parallel/MPI4Py/vtk.module
===================================================================
--- VTK-9.3.0.orig/Parallel/MPI4Py/vtk.module
+++ VTK-9.3.0/Parallel/MPI4Py/vtk.module
@@ -16,4 +16,3 @@ DEPENDS
 PRIVATE_DEPENDS
   VTK::ParallelMPI
   VTK::mpi
-  VTK::mpi4py
