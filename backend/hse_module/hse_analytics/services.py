from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import timedelta, date
from .models import IncidentTrend, SafetyMetrics, LocationStatistics, ComplianceReport
from ..hse_safety.models import Incident, SystemStatus
from ..hse_ptw.models import PermitToWork
from ..hse_pob.models import POBLog, WorkLocation
import logging

logger = logging.getLogger(__name__)


def calculate_incident_trends(period_type='DAILY', days_back=30):
    """
    Calculate incident trends by aggregating from Incident model
    """
    logger.info(f"Calculating incident trends for period: {period_type}")

    today = timezone.now().date()
    start_date = today - timedelta(days=days_back)

    if period_type == 'DAILY':
        # Calculate daily trends
        for i in range(days_back):
            day = today - timedelta(days=i)

            incidents = Incident.objects.filter(
                incident_date__date=day
            )

            trend, created = IncidentTrend.objects.update_or_create(
                period_type='DAILY',
                period_start=day,
                period_end=day,
                defaults={
                    'safety_observation_count': incidents.filter(severity='SAFETY_OBSERVATION').count(),
                    'near_miss_count': incidents.filter(severity='NEAR_MISS').count(),
                    'first_aid_count': incidents.filter(severity='FIRST_AID').count(),
                    'lti_count': incidents.filter(severity='LTI').count(),
                    'total_incidents': incidents.count(),
                    'average_response_time': calculate_avg_response_time(incidents)
                }
            )

            if created:
                logger.info(f"Created daily trend for {day}")

    elif period_type == 'WEEKLY':
        # Calculate weekly trends (last 8 weeks)
        for i in range(8):
            week_start = today - timedelta(weeks=i, days=today.weekday())
            week_end = week_start + timedelta(days=6)

            incidents = Incident.objects.filter(
                incident_date__date__gte=week_start,
                incident_date__date__lte=week_end
            )

            trend, created = IncidentTrend.objects.update_or_create(
                period_type='WEEKLY',
                period_start=week_start,
                period_end=week_end,
                defaults={
                    'safety_observation_count': incidents.filter(severity='SAFETY_OBSERVATION').count(),
                    'near_miss_count': incidents.filter(severity='NEAR_MISS').count(),
                    'first_aid_count': incidents.filter(severity='FIRST_AID').count(),
                    'lti_count': incidents.filter(severity='LTI').count(),
                    'total_incidents': incidents.count(),
                    'average_response_time': calculate_avg_response_time(incidents)
                }
            )

    elif period_type == 'MONTHLY':
        # Calculate monthly trends (last 12 months)
        for i in range(12):
            month_start = date(today.year, today.month, 1) - timedelta(days=30 * i)
            if month_start.month == 12:
                month_end = date(month_start.year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(month_start.year, month_start.month + 1, 1) - timedelta(days=1)

            incidents = Incident.objects.filter(
                incident_date__date__gte=month_start,
                incident_date__date__lte=month_end
            )

            trend, created = IncidentTrend.objects.update_or_create(
                period_type='MONTHLY',
                period_start=month_start,
                period_end=month_end,
                defaults={
                    'safety_observation_count': incidents.filter(severity='SAFETY_OBSERVATION').count(),
                    'near_miss_count': incidents.filter(severity='NEAR_MISS').count(),
                    'first_aid_count': incidents.filter(severity='FIRST_AID').count(),
                    'lti_count': incidents.filter(severity='LTI').count(),
                    'total_incidents': incidents.count(),
                    'average_response_time': calculate_avg_response_time(incidents)
                }
            )

    logger.info(f"Completed calculating {period_type} incident trends")


def calculate_avg_response_time(incidents):
    """
    Calculate average response time for closed incidents
    """
    closed_incidents = incidents.filter(status='CLOSED', closed_date__isnull=False)

    if not closed_incidents.exists():
        return None

    total_hours = 0
    count = 0

    for incident in closed_incidents:
        if incident.closed_date and incident.reported_date:
            delta = incident.closed_date - incident.reported_date
            total_hours += delta.total_seconds() / 3600
            count += 1

    return total_hours / count if count > 0 else None


def calculate_safety_metrics(target_date=None):
    """
    Calculate daily safety metrics from operational data
    """
    if target_date is None:
        target_date = timezone.now().date()

    logger.info(f"Calculating safety metrics for {target_date}")

    # Get system status
    system_status, _ = SystemStatus.get_or_create_singleton()

    # Calculate POB (count unique employees with IN status on target date)
    pob_logs = POBLog.objects.filter(timestamp__date=target_date)

    # Get latest status for each employee
    employee_status = {}
    for log in pob_logs.order_by('timestamp'):
        employee_status[log.emp_id] = log.action

    total_pob = sum(1 for status in employee_status.values() if status == 'IN')

    # PTW statistics for the day
    ptw_issued = PermitToWork.objects.filter(created_at__date=target_date).count()
    ptw_completed = PermitToWork.objects.filter(
        status='CLOSED',
        closed_at__date=target_date
    ).count()
    ptw_rejected = PermitToWork.objects.filter(
        status='REJECTED',
        updated_at__date=target_date
    ).count()

    # Calculate average PTW duration for completed PTWs
    completed_ptws = PermitToWork.objects.filter(
        status='CLOSED',
        closed_at__date=target_date,
        approved_at__isnull=False
    )

    avg_ptw_duration = None
    if completed_ptws.exists():
        total_duration = 0
        count = 0
        for ptw in completed_ptws:
            if ptw.closed_at and ptw.approved_at:
                delta = ptw.closed_at - ptw.approved_at
                total_duration += delta.total_seconds() / 3600
                count += 1
        avg_ptw_duration = total_duration / count if count > 0 else None

    # Incident statistics
    incidents = Incident.objects.filter(incident_date__date=target_date)
    near_misses = incidents.filter(severity='NEAR_MISS').count()
    total_incidents = incidents.count()

    # Calculate LTIFR using 30-day rolling average POB for accuracy
    # This provides more stable and meaningful safety rates
    last_30_days = target_date - timedelta(days=30)

    # Get all POB logs from last 30 days
    pob_logs_30d = POBLog.objects.filter(
        timestamp__date__gte=last_30_days,
        timestamp__date__lte=target_date
    )

    # Count unique employees who worked in last 30 days
    unique_employees_30d = pob_logs_30d.values('emp_id').distinct().count()
    avg_pob_30d = unique_employees_30d / 30 if unique_employees_30d > 0 else 0

    # Calculate LTI count for last 30 days
    lti_count_30d = Incident.objects.filter(
        incident_date__date__gte=last_30_days,
        incident_date__date__lte=target_date,
        severity='LTI'
    ).count()

    # Calculate hours worked over 30 days (12-hour shifts)
    hours_worked_30d = avg_pob_30d * 12 * 30

    # LTIFR = (Number of LTIs × 1,000,000) / Total hours worked
    ltifr = (lti_count_30d * 1000000) / hours_worked_30d if hours_worked_30d > 0 else 0

    # TRIFR = LTIFR × 2.5 (simplified calculation)
    trifr = ltifr * 2.5

    # Determine global status
    if lti_count_30d > 0 or total_incidents > 5:
        global_status = 'RED'
    elif near_misses > 1 or total_incidents > 2:
        global_status = 'YELLOW'
    else:
        global_status = 'GREEN'

    # Create or update safety metrics
    metrics, created = SafetyMetrics.objects.update_or_create(
        date=target_date,
        defaults={
            'total_pob': total_pob,
            'total_ptw_issued': ptw_issued,
            'total_ptw_completed': ptw_completed,
            'total_ptw_rejected': ptw_rejected,
            'average_ptw_duration': avg_ptw_duration,
            'days_without_lti': system_status.days_without_lti,
            'near_misses_count': near_misses,
            'total_incidents': total_incidents,
            'ltifr': ltifr,
            'trifr': trifr,
            'global_status': global_status
        }
    )

    logger.info(f"{'Created' if created else 'Updated'} safety metrics for {target_date}")
    return metrics


def calculate_location_statistics(target_date=None):
    """
    Calculate location statistics from POB logs
    """
    if target_date is None:
        target_date = timezone.now().date()

    logger.info(f"Calculating location statistics for {target_date}")

    locations = WorkLocation.objects.all()

    for location in locations:
        # Get POB logs for this location on target date
        logs = POBLog.objects.filter(
            deck_location=location,
            timestamp__date=target_date
        )

        check_ins = logs.filter(action='IN').count()
        check_outs = logs.filter(action='OUT').count()

        # Calculate occupancy (simplified - count IN actions minus OUT actions)
        occupancy_changes = []
        current_occupancy = 0

        for log in logs.order_by('timestamp'):
            if log.action == 'IN':
                current_occupancy += 1
            else:
                current_occupancy = max(0, current_occupancy - 1)
            occupancy_changes.append(current_occupancy)

        avg_occupancy = sum(occupancy_changes) / len(occupancy_changes) if occupancy_changes else 0
        peak_occupancy = max(occupancy_changes) if occupancy_changes else 0

        # Count incidents at this location
        incidents = Incident.objects.filter(
            location=location,
            incident_date__date=target_date
        ).count()

        # Count PTWs for this location
        ptw_issued = PermitToWork.objects.filter(
            deck_location=location.deck_name,
            created_at__date=target_date
        ).count()

        # Create or update location statistics
        stats, created = LocationStatistics.objects.update_or_create(
            location_name=location.deck_name,
            date=target_date,
            defaults={
                'total_check_ins': check_ins,
                'total_check_outs': check_outs,
                'average_occupancy': avg_occupancy,
                'peak_occupancy': peak_occupancy,
                'total_incidents': incidents,
                'total_ptw_issued': ptw_issued
            }
        )

        # Calculate and save risk score
        stats.calculate_risk_score()
        stats.save()

        logger.info(f"{'Created' if created else 'Updated'} statistics for {location.deck_name}")


def aggregate_all_analytics():
    """
    Main function to aggregate all analytics data
    Called by periodic scheduler
    """
    logger.info("Starting analytics aggregation...")

    try:
        # Calculate today's metrics
        today = timezone.now().date()

        # Calculate safety metrics for today
        calculate_safety_metrics(today)

        # Calculate location statistics for today
        calculate_location_statistics(today)

        # Calculate incident trends (daily for last 30 days)
        calculate_incident_trends('DAILY', days_back=30)

        # Calculate weekly trends (last 8 weeks)
        calculate_incident_trends('WEEKLY')

        # Calculate monthly trends (last 12 months)
        calculate_incident_trends('MONTHLY')

        logger.info("Analytics aggregation completed successfully")

    except Exception as e:
        logger.error(f"Error during analytics aggregation: {str(e)}")
        raise


def update_analytics_realtime(target_date=None):
    """
    Update analytics data in real-time when incidents/PTW change
    Only updates today's data for faster response
    """
    if target_date is None:
        target_date = timezone.now().date()

    logger.info(f"Updating analytics in real-time for {target_date}")

    try:
        # Update safety metrics for today
        calculate_safety_metrics(target_date)

        # Update location statistics for today
        calculate_location_statistics(target_date)

        # Update daily incident trends for today
        today = target_date
        incidents = Incident.objects.filter(incident_date__date=today)

        IncidentTrend.objects.update_or_create(
            period_type='DAILY',
            period_start=today,
            period_end=today,
            defaults={
                'safety_observation_count': incidents.filter(severity='SAFETY_OBSERVATION').count(),
                'near_miss_count': incidents.filter(severity='NEAR_MISS').count(),
                'first_aid_count': incidents.filter(severity='FIRST_AID').count(),
                'lti_count': incidents.filter(severity='LTI').count(),
                'total_incidents': incidents.count(),
                'average_response_time': calculate_avg_response_time(incidents)
            }
        )

        # Calculate compliance report for today
        calculate_compliance_report(target_date)

        logger.info(f"Real-time analytics update completed for {target_date}")

    except Exception as e:
        logger.error(f"Error during real-time analytics update: {str(e)}")
        raise


def calculate_compliance_report(target_date=None):
    """
    Auto-calculate daily compliance report based on system data
    Evaluates: PTW compliance, Incident compliance, POB compliance, Safety status
    """
    if target_date is None:
        target_date = timezone.now().date()

    logger.info(f"Calculating compliance report for {target_date}")

    checks = []
    passed_checks = 0
    total_checks = 0

    # ===== CHECK 1: PTW Signature Compliance =====
    total_checks += 1
    ptws_with_signature = PermitToWork.objects.filter(
        created_at__date=target_date,
        signature__isnull=False
    ).count()
    total_ptws = PermitToWork.objects.filter(created_at__date=target_date).count()

    if total_ptws > 0:
        signature_compliance = (ptws_with_signature / total_ptws) * 100
        if signature_compliance >= 90:
            checks.append(f"PTW Signature Compliance: {signature_compliance:.1f}% ✓")
            passed_checks += 1
        else:
            checks.append(f"PTW Signature Compliance: {signature_compliance:.1f}% ✗")
    else:
        checks.append("PTW Signature Compliance: No PTWs created ✓")
        passed_checks += 1

    # ===== CHECK 2: PTW Approval Compliance =====
    total_checks += 1
    approved_ptws = PermitToWork.objects.filter(
        created_at__date=target_date,
        status__in=['APPROVED', 'IN_PROGRESS', 'WAITING_FOR_CLOSE', 'CLOSED']
    ).count()

    if total_ptws > 0:
        approval_compliance = (approved_ptws / total_ptws) * 100
        if approval_compliance >= 80:
            checks.append(f"PTW Approval Compliance: {approval_compliance:.1f}% ✓")
            passed_checks += 1
        else:
            checks.append(f"PTW Approval Compliance: {approval_compliance:.1f}% ✗")
    else:
        checks.append("PTW Approval Compliance: No PTWs created ✓")
        passed_checks += 1

    # ===== CHECK 3: Incident Reporting Compliance =====
    total_checks += 1
    incidents = Incident.objects.filter(incident_date__date=target_date)
    lti_count = incidents.filter(severity='LTI').count()

    if lti_count == 0:
        checks.append(f"No LTI Incidents: {incidents.count()} incidents reported ✓")
        passed_checks += 1
    else:
        checks.append(f"LTI Incidents Found: {lti_count} LTI(s) ✗")

    # ===== CHECK 4: Incident Closure Compliance =====
    total_checks += 1
    closed_incidents = incidents.filter(status='CLOSED').count()
    total_incidents = incidents.count()

    if total_incidents > 0:
        closure_rate = (closed_incidents / total_incidents) * 100
        if closure_rate >= 70:
            checks.append(f"Incident Closure Rate: {closure_rate:.1f}% ✓")
            passed_checks += 1
        else:
            checks.append(f"Incident Closure Rate: {closure_rate:.1f}% ✗")
    else:
        checks.append("Incident Closure Rate: No incidents ✓")
        passed_checks += 1

    # ===== CHECK 5: POB Check-in/out Compliance =====
    total_checks += 1
    pob_logs = POBLog.objects.filter(timestamp__date=target_date)
    employees = set(log.emp_id for log in pob_logs)

    if employees:
        # Check if employees have both IN and OUT
        compliant_employees = 0
        for emp_id in employees:
            emp_logs = pob_logs.filter(emp_id=emp_id).order_by('timestamp')
            actions = list(emp_logs.values_list('action', flat=True))
            # Should have IN and OUT or just IN (still working)
            if 'IN' in actions:
                compliant_employees += 1

        pob_compliance = (compliant_employees / len(employees)) * 100
        if pob_compliance >= 95:
            checks.append(f"POB Check-in Compliance: {pob_compliance:.1f}% ✓")
            passed_checks += 1
        else:
            checks.append(f"POB Check-in Compliance: {pob_compliance:.1f}% ✗")
    else:
        checks.append("POB Check-in Compliance: No POB activity ✓")
        passed_checks += 1

    # ===== CHECK 6: System Status Compliance =====
    total_checks += 1
    try:
        system_status = SystemStatus.objects.get(id=1)
        if system_status.global_status == 'GREEN':
            checks.append(f"System Status: GREEN ✓")
            passed_checks += 1
        elif system_status.global_status == 'YELLOW':
            checks.append(f"System Status: YELLOW (Warning) ⚠")
        else:
            checks.append(f"System Status: RED (Emergency) ✗")
    except SystemStatus.DoesNotExist:
        checks.append("System Status: Not configured ✓")
        passed_checks += 1

    # ===== CHECK 7: PTW Closure Compliance =====
    total_checks += 1
    closed_ptws = PermitToWork.objects.filter(
        created_at__date=target_date,
        status='CLOSED'
    ).count()

    if total_ptws > 0:
        closure_compliance = (closed_ptws / total_ptws) * 100
        if closure_compliance >= 50:  # At least 50% should be closed same day
            checks.append(f"PTW Same-Day Closure: {closure_compliance:.1f}% ✓")
            passed_checks += 1
        else:
            checks.append(f"PTW Same-Day Closure: {closure_compliance:.1f}% ⚠")
    else:
        checks.append("PTW Same-Day Closure: No PTWs created ✓")
        passed_checks += 1

    # ===== Calculate Overall Compliance Score =====
    compliance_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0

    # Determine overall status
    if compliance_score >= 90:
        overall_status = 'COMPLIANT'
    elif compliance_score >= 70:
        overall_status = 'PARTIAL'
    else:
        overall_status = 'NON_COMPLIANT'

    # Get auditor info (system auto-audit)
    auditor_name = "System Auto-Audit"
    auditor_emp_id = "SYSTEM"

    # Create or update compliance report
    report, created = ComplianceReport.objects.update_or_create(
        report_type='DAILY',
        report_date=target_date,
        defaults={
            'period_start': target_date,
            'period_end': target_date,
            'overall_status': overall_status,
            'compliance_score': compliance_score,
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': total_checks - passed_checks,
            'findings': '\n'.join(checks),
            'recommendations': generate_compliance_recommendations(overall_status, checks),
            'auditor_name': auditor_name,
            'auditor_emp_id': auditor_emp_id
        }
    )

    logger.info(f"{'Created' if created else 'Updated'} compliance report for {target_date}: Score={compliance_score:.1f}%, Status={overall_status}")
    return report


def generate_compliance_recommendations(status, checks):
    """
    Generate recommendations based on compliance status and failed checks
    """
    recommendations = []

    if status == 'NON_COMPLIANT':
        recommendations.append("URGENT: Multiple compliance issues detected. Immediate action required.")
        recommendations.append("Review all failed checks and implement corrective actions.")
        recommendations.append("Conduct management review and safety briefing.")

    elif status == 'PARTIAL':
        recommendations.append("Several compliance gaps identified. Schedule corrective actions.")
        recommendations.append("Focus on areas with lower compliance rates.")
        recommendations.append("Increase monitoring and supervision in critical areas.")

    else:  # COMPLIANT
        recommendations.append("Maintain current safety standards and procedures.")
        recommendations.append("Continue regular monitoring and audits.")
        recommendations.append("Share best practices with team members.")

    # Add specific recommendations based on failed checks
    failed_checks = [c for c in checks if '✗' in c]
    if failed_checks:
        recommendations.append("\nSpecific Areas for Improvement:")
        for check in failed_checks:
            recommendations.append(f"- {check}")

    return '\n'.join(recommendations)
