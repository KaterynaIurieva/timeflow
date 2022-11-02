{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "timeflow.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "timeflow.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "timeflow.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "timeflow.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "timeflow.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create the full image name
*/}}
{{- define "timeflow.image" -}}
{{- if ne .digest "" }}
{{- printf "%s/%s:%s@%s" .repository .imageName .tag .digest -}}
{{- else }}
{{- printf "%s/%s:%s" .repository .imageName .tag -}}
{{- end -}}
{{- end -}}

{{/*
Returns a set of labels applied to each resource.
*/}}
{{- define "timeflow.labels" -}}
app.kubernetes.io/name: {{ template "timeflow.name" . }}
chart: {{ template "timeflow.chart" . }}
release: {{ .Release.Name }}
{{- end -}}

{{/*
Returns a set of labels applied to each resource.
*/}}
{{- define "timeflow.db.labels" -}}
{{ include "timeflow.labels" . }}
component: db
{{- end -}}

{{/*
Returns a set of labels applied to each resource.
*/}}
{{- define "timeflow.fastapi.labels" -}}
{{ include "timeflow.labels" . }}
component: fastapi
{{- end -}}

{{/*
Returns a set of labels applied to each resource.
*/}}
{{- define "timeflow.frontend.labels" -}}
{{ include "timeflow.labels" . }}
component: frontend
{{- end -}}


