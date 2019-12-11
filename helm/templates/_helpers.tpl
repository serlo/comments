{{/*
Expand the name of the chart.
*/}}
{{- define "comments.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "comments.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Default labels to be used for resources
*/}}
{{- define "comments.labels" }}
app: {{ template "comments.name" . }}
chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
release: {{ .Release.Name }}
heritage: {{ .Release.Service }}
{{- end }}

{{/*
Database host depending on whether an external database is used
*/}}
{{- define "comments.database.host" -}}
{{- if .Values.postgresql.enabled -}}
{{ $.Release.Name }}-postgresql-headless
{{- else -}}
{{- .Values.externalPostgresql.host -}}
{{- end -}}
{{- end -}}

{{/*
Database port depending on whether an external database is used
*/}}
{{- define "comments.database.port" -}}
{{- if .Values.postgresql.enabled -}}
{{- .Values.postgresql.service.port -}}
{{- else -}}
{{- .Values.externalPostgresql.port -}}
{{- end -}}
{{- end -}}

{{/*
Database name depending on whether an external database is used
*/}}
{{- define "comments.database.name" -}}
{{- if .Values.postgresql.enabled -}}
{{- .Values.postgresql.postgresqlDatabase -}}
{{- else -}}
{{- .Values.externalPostgresql.database -}}
{{- end -}}
{{- end -}}

{{/*
Database user depending on whether an external database is used
*/}}
{{- define "comments.database.user" -}}
{{- if .Values.postgresql.enabled -}}
{{- .Values.postgresql.postgresqlUsername -}}
{{- else -}}
{{- .Values.externalPostgresql.username -}}
{{- end -}}
{{- end -}}

{{/*
Database password depending on whether an external database is used
*/}}
{{- define "comments.database.password" }}
{{- if .Values.postgresql.enabled -}}
{{- .Values.postgresql.postgresqlPassword -}}
{{- else -}}
{{- .Values.externalPostgresql.password -}}
{{- end -}}
{{- end -}}
