from rest_framework import serializers
from .models import IncidentTrend, SafetyMetrics, ComplianceReport, LocationStatistics


class IncidentTrendSerializer(serializers.ModelSerializer):
    """
    Serializer for incident trend analytics
    """
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = IncidentTrend
        fields = [
            'id',
            'period_type',
            'period_start',
            'period_end',
            'vessel',
            'vessel_name',
            'safety_observation_count',
            'near_miss_count',
            'first_aid_count',
            'lti_count',
            'total_incidents',
            'days_without_lti',
            'average_response_time',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'vessel_name']


class SafetyMetricsSerializer(serializers.ModelSerializer):
    """
    Serializer for safety performance metrics
    """
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = SafetyMetrics
        fields = [
            'id',
            'date',
            'vessel',
            'vessel_name',
            'total_pob',
            'total_ptw_issued',
            'total_ptw_completed',
            'total_ptw_rejected',
            'average_ptw_duration',
            'days_without_lti',
            'near_misses_count',
            'total_incidents',
            'ltifr',
            'trifr',
            'global_status',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'vessel_name']


class ComplianceReportSerializer(serializers.ModelSerializer):
    """
    Serializer for ISO 45001 compliance reports
    """
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = ComplianceReport
        fields = [
            'id',
            'report_type',
            'report_date',
            'period_start',
            'period_end',
            'vessel',
            'vessel_name',
            'overall_status',
            'compliance_score',
            'total_checks',
            'passed_checks',
            'failed_checks',
            'findings',
            'recommendations',
            'auditor_name',
            'auditor_emp_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'vessel_name']

    def create(self, validated_data):
        """
        Create compliance report and auto-calculate compliance score
        """
        report = ComplianceReport.objects.create(**validated_data)
        report.calculate_compliance_score()
        report.save()
        return report


class LocationStatisticsSerializer(serializers.ModelSerializer):
    """
    Serializer for location-based statistics
    """
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = LocationStatistics
        fields = [
            'id',
            'location_name',
            'date',
            'vessel',
            'vessel_name',
            'total_check_ins',
            'total_check_outs',
            'average_occupancy',
            'peak_occupancy',
            'total_incidents',
            'total_ptw_issued',
            'risk_score',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'vessel_name']

    def create(self, validated_data):
        """
        Create location statistics and auto-calculate risk score
        """
        stats = LocationStatistics.objects.create(**validated_data)
        stats.calculate_risk_score()
        stats.save()
        return stats
