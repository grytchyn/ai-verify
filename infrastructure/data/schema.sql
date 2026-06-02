-- AI-Verify v2.0 — Database Schema (PostgreSQL)
-- This file contains the complete database schema for AI-Verify
-- Run with: psql -d ai_verify -f schema.sql

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ==========================================
-- CORE TABLES
-- ==========================================

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'analyst', -- analyst, admin,superadmin
    avatar_url TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);

-- Organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    domain VARCHAR(255),
    plan VARCHAR(50) DEFAULT 'free', -- free,trial,pro,enterprise,unicorn
    seats INT DEFAULT 1,
    ai_systems_count INT DEFAULT 0,
    dpo_name VARCHAR(255),
    dpo_email VARCHAR(255),
    dpo_verified BOOLEAN DEFAULT FALSE,
    dpo_verified_at TIMESTAMPTZ,
    stripe_customer_id VARCHAR(255),
    features JSONB DEFAULT jsonb_build_object(),
    limits JSONB DEFAULT jsonb_build_object(
        'monthly_checks', 3,
        'storage_gb', 0.1,
        'team_members', 1
    ),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_orgs_plan ON organizations(plan);
CREATE INDEX idx_orgs_created ON organizations(created_at);

-- User-Org relationship (Many-to-Many)
CREATE TABLE user_organizations (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member', -- owner, admin, member
    accepted BOOLEAN DEFAULT FALSE,
    invited_at TIMESTAMPTZ,
    joined_at TIMESTAMPTZ,
    PRIMARY KEY (user_id, org_id)
);

CREATE INDEX idx_user_orgs_user ON user_organizations(user_id);
CREATE INDEX idx_user_orgs_org ON user_organizations(org_id);

-- ==========================================
-- COMPLIANCE CHECKS
-- ==========================================

-- Compliance Check (main record)
CREATE TABLE compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    
    -- Input data
    url VARCHAR(255) NOT NULL,
    website_title VARCHAR(255),
    website_domain VARCHAR(255),
    website_language VARCHAR(10) DEFAULT 'en',
    
    -- Analysis results
    score INT CHECK (score >= 0 AND score <= 100),
    risk_level VARCHAR(20) CHECK (risk_level IN ('unacceptable', 'high', 'limited', 'minimal', 'unknown')),
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed, rejected
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    ai_signals TEXT[],
    
    -- Report data
    recommendations TEXT[],
    ai_act_references TEXT[],
    high_risk_categories TEXT[],
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_checks_org ON compliance_checks(org_id);
CREATE INDEX idx_checks_user ON compliance_checks(user_id);
CREATE INDEX idx_checks_status ON compliance_checks(status);
CREATE INDEX idx_checks_created ON compliance_checks(created_at DESC);
CREATE INDEX idx_checks_url ON compliance_checks(url);

-- Comments/Notes on checks
CREATE TABLE check_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    check_id UUID REFERENCES compliance_checks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    org_id UUID REFERENCES organizations(id),
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_comments_check ON check_comments(check_id);
CREATE INDEX idx_comments_user ON check_comments(user_id);

-- ==========================================
-- AI SYSTEMS
-- ==========================================

CREATE TABLE ai_systems (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    check_id UUID REFERENCES compliance_checks(id) ON DELETE CASCADE,
    
    -- System info
    name VARCHAR(255),
    description TEXT,
    domain VARCHAR(255),
    
    -- Classification
    deployment_type VARCHAR(50), -- internal, customer-facing, both
    decision_type VARCHAR(50), -- fully-automated, human-in-the-loop, decision-support, recommendation
    risk_self_assessment VARCHAR(50), -- minimal, limited, high, unacceptable, unknown
    
    -- Risk details
    risk_factors TEXT[],
    mitigation_measures TEXT[],
    
    -- AI Act alignment
    ai_act_references TEXT[],
    compliance_notes TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ai_systems_check ON ai_systems(check_id);

-- High-Risk Categories (reference data)
CREATE TABLE high_risk_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- AI Act references
    ai_act_articles TEXT[],
    risk_class VARCHAR(20) DEFAULT 'high', -- high, unacceptable
    
    -- Evidence requirements
    evidence_required JSONB DEFAULT '{}'::jsonb,
    example_evidence TEXT[],
    
    -- Status
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_categories_code ON high_risk_categories(code);

-- AI System - High-Risk Category linkage
CREATE TABLE ai_system_categories (
    ai_system_id UUID REFERENCES ai_systems(id) ON DELETE CASCADE,
    category_id UUID REFERENCES high_risk_categories(id) ON DELETE CASCADE,
    risk_level VARCHAR(20) DEFAULT 'high',
    mitigation TEXT,
    PRIMARY KEY (ai_system_id, category_id)
);

CREATE INDEX idx_sys_categories_system ON ai_system_categories(ai_system_id);

-- ==========================================
-- COMPLIANCE DOCUMENTATION
-- ==========================================

CREATE TABLE compliance_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    check_id UUID REFERENCES compliance_checks(id) ON DELETE CASCADE,
    
    -- Document info
    doc_type VARCHAR(50), -- policy, risk-assessment, transparency, security
    title VARCHAR(255),
    description TEXT,
    
    -- Content
    content TEXT,
    content_html TEXT,
    
    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, completed, certified, outdated
    certified_at TIMESTAMPTZ,
    certified_by UUID REFERENCES users(id),
    
    -- Versioning
    version INT DEFAULT 1,
    is_latest BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_docs_check ON compliance_documents(check_id);
CREATE INDEX idx_docs_type ON compliance_documents(doc_type);
CREATE INDEX idx_docs_status ON compliance_documents(status);

-- ==========================================
-- DPO REGISTRY
-- ==========================================

CREATE TABLE dp_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID UNIQUE NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    dpo_name VARCHAR(255) NOT NULL,
    dpo_email VARCHAR(255) NOT NULL,
    dpo_phone VARCHAR(50),
    dpo_address TEXT,
    dpo_verified BOOLEAN DEFAULT FALSE,
    dpo_verified_at TIMESTAMPTZ,
    verification_method VARCHAR(50), -- manual, automated, third-party
    notes TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- AUDIT TRAIL
-- ==========================================

CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    
    -- Action info
    event_type VARCHAR(100), -- created, updated, deleted, certified, flagged
    event_category VARCHAR(50), -- compliance_check, ai_system, document, user
    event_entity_id UUID,
    
    -- Details (full JSON)
    before_state JSONB,
    after_state JSONB,
    details JSONB,
    
    -- IP/User agent
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audits_org ON audits(org_id);
CREATE INDEX idx_audits_user ON audits(user_id);
CREATE INDEX idx_audits_event ON audits(event_type);
CREATE INDEX idx_audits_timestamp ON audits(created_at DESC);

-- ==========================================
-- SUBSCRIPTIONS & BILLING
-- ==========================================

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID UNIQUE NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    -- Stripe info
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    
    -- Plan info
    plan VARCHAR(50) NOT NULL, -- free,trial,pro,enterprise,unicorn
    status VARCHAR(50) DEFAULT 'active', -- active,cancel_schedule,past_due,unpaid,deleted
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    
    -- Usage tracking
    checks_used INT DEFAULT 0,
    checks_limit INT DEFAULT 3,
    storage_used_gb DECIMAL(10,2) DEFAULT 0.0,
    storage_limit_gb DECIMAL(10,2) DEFAULT 0.1,
    
    -- Autobilling
    auto_renew BOOLEAN DEFAULT TRUE,
    payment_method_last4 VARCHAR(4),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- FEATURE FLAGS
-- ==========================================

CREATE TABLE feature_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    enabled BOOLEAN DEFAULT FALSE,
    environment VARCHAR(50) DEFAULT 'production', -- development,staging,production
    rollout_percent INT DEFAULT 100,
    audience JSONB DEFAULT jsonb_build_object('all', true),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- UTILIZATION METERING (Materialized View)
-- ==========================================

CREATE MATERIALIZED VIEW compliance_stats AS
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS total_checks,
        AVG(score) AS avg_score,
        COUNT(*) FILTER (WHERE risk_level IN ('high', 'unacceptable')) AS high_risk_count,
        COUNT(*) FILTER (WHERE risk_level = 'unacceptable') AS unacceptable_risk_count
    FROM compliance_checks
    GROUP BY DATE_TRUNC('month', created_at)
)
SELECT m.*, o.org_count,
       o.active_users,
       o.total_ai_systems
FROM monthly m
LEFT JOIN LATERAL (
    SELECT 
        COUNT(DISTINCT org_id) AS org_count,
        COUNT(DISTINCT user_id) AS active_users,
        SUM(ai_systems_count) AS total_ai_systems
    FROM organizations
    WHERE created_at <= m.month + INTERVAL '1 month'
) o ON TRUE
ORDER BY m.month DESC;

CREATE INDEX idx_stats_month ON compliance_stats (month DESC);

-- ==========================================
-- TRIGGERS
-- ==========================================

-- Update updated_at on row change
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orgs_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_checks_updated_at BEFORE UPDATE ON compliance_checks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_systems_updated_at BEFORE UPDATE ON ai_systems
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_docs_updated_at BEFORE UPDATE ON compliance_documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dpo_updated_at BEFORE UPDATE ON dp_registry
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==========================================
-- SEED DATA (for development)
-- ==========================================

INSERT INTO high_risk_categories (code, name, description, ai_act_articles, risk_class, example_evidence)
VALUES
    ('biometric', 'Remote Biometric Identification', 'Identification of persons by means of biometrics', ARRAY['Art. 5(1)(b)'], 'unacceptable', ARRAY['Legal basis', 'Necessity assessment', 'Proportionality test']),
    ('crediting', 'Credit Scoring', 'Evaluation of creditworthiness', ARRAY['Art. 6(1)(a)'], 'high', ARRAY['Data quality report', 'Risk assessment', 'Transparency notice']),
    ('education', 'Education/Vocational Training', 'AI in education settings', ARRAY['Art. 6(1)(c)'], 'high', ARRAY['Pedagogical impact assessment', 'Student consent', 'Transparency log']),
    ('employment', 'Recruitment/Selection', 'AI in hiring', ARRAY['Art. 6(1)(d)'], 'high', ARRAY['Bias audit report', 'Job description review', 'Selection criteria log']),
    ('law_enforcement', 'Law Enforcement', 'AI for law enforcement', ARRAY['Art. 6(1)(e)'], 'high', ARRAY['Necessity/proportionality test', 'Legal basis', 'Independent oversight']),
    ('critical_infra', 'Critical Infrastructure', 'AI in critical infrastructure', ARRAY['Art. 6(1)(f)'], 'high', ARRAY['Risk assessment', 'Incident response plan', 'Cybersecurity report']),
    ('mig_asyl', 'Migration/Asylum', 'AI in migration decisions', ARRAY['Art. 6(1)(g)'], 'high', ARRAY['Bias assessment', 'Individual review log', 'Appeal process']),
    ('marshalling', 'Marshalling/Policing', 'AI in transportation control', ARRAY['Art. 6(1)(h)'], 'high', ARRAY['Safety assessment', 'Operator training log', 'Incident history']);
    
COMMENT ON TABLE compliance_checks IS 'Main compliance assessment records';
COMMENT ON TABLE ai_systems IS 'Detailed AI system information from compliance assessment';
COMMENT ON TABLE high_risk_categories IS 'Reference table for EU AI Act high-risk categories';
COMMENT ON TABLE audits IS 'Complete audit trail for all compliance decisions';
