# Amazon Rekognition - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Rekognition is a cloud-based image and video analysis service powered by deep learning. With simple APIs you can detect objects, scenes, text, faces, celebrities, and unsafe content in images and videos stored in S3, without ML expertise. It is HIPAA-eligible and uses pay-as-you-go pricing.

## Key concepts

- **Image analysis**: object/scene/concept detection, text detection, unsafe content moderation, celebrity recognition, facial analysis, image properties (quality, color, sharpness), and Custom Labels classifiers.
- **Video analysis**: object/scene/concept detection, text detection, people pathing, face analysis, celebrity recognition, unsafe content, video segmentation, and face liveness.
- **Face collections**: containers for indexing and searching faces for facial search and identity verification.
- **Face Liveness**: fully managed feature that verifies a live user is physically present, detecting spoofs (photos, videos, 3D masks, deepfakes).
- **Content moderation**: hierarchical labels with confidence scores for filtering user-generated content; customizable with adapters.
- **Custom Labels**: train custom classifiers for domain-specific objects (logos, products, characters) without ML expertise.
- **PPE detection**: detect personal protective equipment to monitor safety compliance.
- **Integrations**: works with S3, Lambda, IAM; analyze images/videos without moving data.

## Common operations (AWS CLI)

```bash
# Image analysis
aws rekognition detect-labels --image '{"S3Object":{"Bucket":"bucket","Name":"photo.jpg"}}'
aws rekognition detect-text --image '{"S3Object":{"Bucket":"bucket","Name":"sign.jpg"}}'
aws rekognition detect-moderation-labels --image '{"S3Object":{"Bucket":"bucket","Name":"photo.jpg"}}'

# Face operations
aws rekognition create-collection --collection-id users
aws rekognition index-faces --collection-id users \
  --image '{"S3Object":{"Bucket":"bucket","Name":"face.jpg"}}'
aws rekognition search-faces-by-image --collection-id users \
  --image '{"S3Object":{"Bucket":"bucket","Name":"probe.jpg"}}'

# Video analysis (async, results to SNS)
aws rekognition start-label-detection --video '{"S3Object":{"Bucket":"bucket","Name":"clip.mp4"}}' \
  --notification-channel file://sns.json
aws rekognition get-label-detection --job-id <job-id>
```

## Best practices

- Store media in S3 with lifecycle policies; analyze in place with IAM-scoped roles.
- Use content moderation with adapters for user-generated content platforms; set confidence thresholds.
- Use Face Liveness for identity verification to deter spoofing; follow applicable privacy laws and get consent where required.
- Use Custom Labels for niche objects rather than relying on general labels.
- For video, use async jobs with SNS notifications and monitor job completion.
- Combine with Lambda and EventBridge for automated pipelines (moderation, cataloging).

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| API errors on S3 image | Check bucket permissions, object key, and Region. |
| No faces found | Verify image quality/orientation and face size requirements. |
| Video job stuck | Check the SNS topic permissions and job status; re-submit if needed. |
| Custom Labels accuracy low | Add more labeled training images per category. |
| Moderation misses content | Adjust confidence thresholds or train adapters with sample images. |

## Limits

Image size, face collections per account, video duration, and API request rates have quotas. See the Amazon Rekognition endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Rekognition?](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html)
- [Amazon Rekognition endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/rekognition.html)
- [Amazon Rekognition pricing](https://aws.amazon.com/rekognition/pricing/)
- [AWS CLI: rekognition commands](https://docs.aws.amazon.com/cli/latest/reference/rekognition/)
