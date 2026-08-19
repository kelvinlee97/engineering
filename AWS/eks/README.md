# Amazon EKS - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Elastic Kubernetes Service (Amazon EKS) is a fully managed Kubernetes service. AWS operates the Kubernetes control plane; you can also use **EKS Auto Mode** to let AWS manage nodes, scaling, patching, and security integration.

## Key concepts

- **EKS standard**: AWS manages the control plane; you manage nodes (EC2 managed node groups, Fargate, or self-managed) and workloads.
- **EKS Auto Mode**: AWS also manages the data plane (nodes), provisioning, cost optimization, and patching.
- **EKS Capabilities**: fully managed cluster extensions such as Argo CD (GitOps), AWS Controllers for Kubernetes (ACK), and kro.
- **Access control**: AWS IAM controls access to the Kubernetes API; Kubernetes Service Accounts (IRSA) grant pods AWS permissions.
- **Compute**: all EC2 instance types, including Nitro and Graviton.
- **Storage**: EBS via CSI, plus Amazon EFS, FSx, S3, and S3 Files.
- **Compatibility**: certified Kubernetes-conformant; standard and extended support versions.

## Common operations

```bash
# Create a cluster (IAM role with EKS permissions)
aws eks create-cluster --name my-cluster --role-arn arn:aws:iam::123456789012:role/eks-cluster \
  --resources-vpc-config subnetIds=subnet-xxx,subnet-yyy
aws eks list-clusters
aws eks describe-cluster --name my-cluster

# Point kubectl at the cluster
aws eks update-kubeconfig --name my-cluster --region ap-southeast-1
kubectl get nodes
kubectl get pods -A

# Alternative: eksctl
eksctl create cluster --name my-cluster --region ap-southeast-1 --nodegroup-type managed

# Delete
aws eks delete-cluster --name my-cluster
```

## Best practices

- Grant cluster access through **AWS IAM**; never share long-lived kubeconfig credentials.
- Use **IRSA** or EKS Pod Identity so pods get temporary credentials with least privilege.
- Use **managed node groups** or EKS Auto Mode; keep node AMIs patched.
- Apply Kubernetes Pod Security Standards or a policy engine; scan images.
- Monitor with CloudWatch Container Insights, Amazon Managed Prometheus, and CloudTrail.
- Back up clusters and workloads (for example, Velero) and plan upgrade paths against the Kubernetes version lifecycle.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Node `NotReady` | Check node instance health, kubelet logs, AMI, and security groups/network. |
| Pods `Pending` | Check resource requests, node capacity, taints/tolerations, and storage classes. |
| API server unreachable | Verify VPC networking, security groups, and `update-kubeconfig` context. |
| IRSA `AccessDenied` | Check the pod service account annotation and the role trust policy (`oidc.eks.<region>.amazonaws.com/id/<cluster>`). |
| EBS volume issues | Confirm the EBS CSI driver is installed and the node role has permissions. |
| Upgrade failures | Follow the supported version lifecycle; test on a staging cluster first. |

## Limits

Per-Region quotas apply to clusters, nodes, and Fargate profiles. See the Service Quotas console for current values.

## Official references

- [What is Amazon EKS? - Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
- [eksctl](https://eksctl.io/)
- [AWS CLI: eks commands](https://docs.aws.amazon.com/cli/latest/reference/eks/)
