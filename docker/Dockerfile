# R-013 sandbox: Jupyter Kernel Gateway (the smolagents-ts Docker protocol) plus pytest.
# Versions are recorded after the build (pip freeze), not pinned here.
FROM python:3.12-slim
RUN pip install --no-cache-dir jupyter_kernel_gateway jupyter_client ipykernel pytest
WORKDIR /work
EXPOSE 8888
CMD ["jupyter", "kernelgateway", "--KernelGatewayApp.ip=0.0.0.0", "--KernelGatewayApp.port=8888", "--KernelGatewayApp.allow_origin=*"]
