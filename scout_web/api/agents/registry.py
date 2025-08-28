from .agent_defs import (
    cloud_asset_discovery_agent,
    security_risk_assessment_agent,
    compliance_auditing_agent,
    vulnerability_scanning_agent,
    threat_intelligence_agent,
    incident_response_agent,
    cost_optimization_agent,
    access_control_agent,
    network_security_agent,
    data_security_agent,
)
from .qa_agent_defs import (
    qa_cloud_asset_discovery,
    qa_security_risk_assessment,
    qa_compliance_auditing,
    qa_vulnerability_scanning,
    qa_threat_intelligence,
    qa_incident_response,
    qa_cost_optimization,
    qa_access_control,
    qa_network_security,
    qa_data_security,
)

AGENTS = {
    "cloud_asset_discovery": cloud_asset_discovery_agent,
    "security_risk_assessment": security_risk_assessment_agent,
    "compliance_auditing": compliance_auditing_agent,
    "vulnerability_scanning": vulnerability_scanning_agent,
    "threat_intelligence": threat_intelligence_agent,
    "incident_response": incident_response_agent,
    "cost_optimization": cost_optimization_agent,
    "access_control": access_control_agent,
    "network_security": network_security_agent,
    "data_security": data_security_agent,
}

QA_AGENTS = {
    "cloud_asset_discovery": qa_cloud_asset_discovery,
    "security_risk_assessment": qa_security_risk_assessment,
    "compliance_auditing": qa_compliance_auditing,
    "vulnerability_scanning": qa_vulnerability_scanning,
    "threat_intelligence": qa_threat_intelligence,
    "incident_response": qa_incident_response,
    "cost_optimization": qa_cost_optimization,
    "access_control": qa_access_control,
    "network_security": qa_network_security,
    "data_security": qa_data_security,
}
