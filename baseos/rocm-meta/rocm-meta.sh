export ROC_ENABLE_PRE_VEGA=1

if [ -z "$PATH" ]
then
	PATH="/opt/rocm/bin:/opt/rocm/profiler/bin:/opt/rocm/opencl/bin:/opt/rocm/hip/bin"
elif ! [[ "$PATH" =~ "/opt/rocm/bin:/opt/rocm/profiler/bin:/opt/rocm/opencl/bin:/opt/rocm/hip/bin" ]]
then
    PATH=$PATH":/opt/rocm/bin:/opt/rocm/profiler/bin:/opt/rocm/opencl/bin:/opt/rocm/hip/bin"
fi
export PATH

if [ -z "$LD_LIBRARY_PATH" ]
then
	LD_LIBRARY_PATH="/opt/rocm/lib:/opt/rocm/lib64:/opt/rocm/profiler/lib:/opt/rocm/profiler/lib64:/opt/rocm/opencl/lib:/opt/rocm/hip/lib:/opt/rocm/opencl/lib64:/opt/rocm/hip/lib64"
elif ! [[ "$LD_LIBRARY_PATH" =~ "/opt/rocm/lib:/opt/rocm/lib64:/opt/rocm/profiler/lib:/opt/rocm/profiler/lib64:/opt/rocm/opencl/lib:/opt/rocm/hip/lib:/opt/rocm/opencl/lib64:/opt/rocm/hip/lib64" ]]
then
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH":/opt/rocm/lib:/opt/rocm/lib64:/opt/rocm/profiler/lib:/opt/rocm/profiler/lib64:/opt/rocm/opencl/lib:/opt/rocm/hip/lib:/opt/rocm/opencl/lib64:/opt/rocm/hip/lib64"
fi
export LD_LIBRARY_PATH

