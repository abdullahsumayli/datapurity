import React, { useEffect, useState } from 'react';
import apiClient from '../../config/apiClient';
import { useAuth } from '../../contexts/AuthContext';
import './profile.css';

interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
  total_contacts: number;
  total_jobs: number;
}

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'activity'>('profile');
  
  const [formData, setFormData] = useState({
    full_name: '',
    email: ''
  });

  useEffect(() => {
    loadProfile();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadProfile = async () => {
    try {
      setError(null);
      const response = await apiClient.get('/users/me');
      const profileData = response.data;
      
      setProfile(profileData);
      setFormData({
        full_name: profileData.full_name || '',
        email: profileData.email
      });
    } catch (error: any) {
      console.error('Failed to load profile:', error);
      setError('فشل تحميل الملف الشخصي');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      const response = await apiClient.put('/users/me', formData);
      setProfile(response.data);
      setIsEditing(false);
    } catch (error: any) {
      console.error('Failed to save profile:', error);
      setError('فشل حفظ التعديلات');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (profile) {
      setFormData({
        full_name: profile.full_name || '',
        email: profile.email
      });
    }
    setIsEditing(false);
    setError(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ar-SA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };

  if (loading) {
    return (
      <div className="profile-loading">
        <div className="loading-spinner"></div>
        <p>جاري تحميل الملف الشخصي...</p>
      </div>
    );
  }

  return (
    <div className="profile-page">
      {/* Header Section */}
      <div className="profile-header">
        <div className="profile-header-content">
          <div className="profile-avatar">
            <div className="avatar-circle">
              <span className="avatar-initials">
                {profile?.full_name?.charAt(0).toUpperCase() || profile?.email.charAt(0).toUpperCase() || 'M'}
              </span>
            </div>
            <button className="avatar-upload-btn">
              <span className="icon">📷</span>
              تغيير الصورة
            </button>
          </div>
          
          <div className="profile-header-info">
            <h1>{profile?.full_name || profile?.email.split('@')[0]}</h1>
            <p className="profile-email">{profile?.email}</p>
            <p className="profile-member-since">
              عضو منذ {profile && formatDate(profile.created_at)}
            </p>
          </div>

          {!isEditing && (
            <button className="btn-edit-profile" onClick={() => setIsEditing(true)}>
              <span className="icon">✏️</span>
              تعديل الملف الشخصي
            </button>
          )}
        </div>

        {/* Stats Cards */}
        <div className="profile-stats">
          <div className="stat-card">
            <div className="stat-icon contact-icon">👥</div>
            <div className="stat-content">
              <h3>{profile?.total_contacts || 0}</h3>
              <p>جهات الاتصال</p>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="stat-icon dataset-icon">📊</div>
            <div className="stat-content">
              <h3>{profile?.total_jobs || 0}</h3>
              <p>مهمات المعالجة</p>
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-banner">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}

      {/* Tabs Navigation */}
      <div className="profile-tabs">
        <button 
          className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          <span className="tab-icon">👤</span>
          المعلومات الشخصية
        </button>
        <button 
          className={`tab-btn ${activeTab === 'security' ? 'active' : ''}`}
          onClick={() => setActiveTab('security')}
        >
          <span className="tab-icon">🔒</span>
          الأمان والخصوصية
        </button>
        <button 
          className={`tab-btn ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => setActiveTab('activity')}
        >
          <span className="tab-icon">📈</span>
          النشاط الأخير
        </button>
      </div>

      {/* Tab Content */}
      <div className="profile-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">📝</span>
                المعلومات الأساسية
              </h2>
              
              <div className="form-grid">
                <div className="form-field">
                  <label htmlFor="full_name">الاسم الكامل</label>
                  <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>

                <div className="form-field">
                  <label htmlFor="email">البريد الإلكتروني</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    disabled={!isEditing}
                    className={!isEditing ? 'disabled' : ''}
                  />
                </div>
              </div>

              {isEditing && (
                <div className="form-actions">
                  <button 
                    className="btn-save"
                    onClick={handleSave}
                    disabled={saving}
                  >
                    {saving ? 'جاري الحفظ...' : '💾 حفظ التغييرات'}
                  </button>
                  <button 
                    className="btn-cancel"
                    onClick={handleCancel}
                    disabled={saving}
                  >
                    ❌ إلغاء
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'security' && (
          <div className="profile-section">
            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">🔐</span>
                كلمة المرور
              </h2>
              
              <div className="security-info">
                <p className="info-text">
                  آخر تغيير لكلمة المرور كان منذ 30 يوماً
                </p>
                <button className="btn-change-password">
                  🔑 تغيير كلمة المرور
                </button>
              </div>
            </div>

            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">📱</span>
                المصادقة الثنائية
              </h2>
              
              <div className="security-option">
                <div className="option-info">
                  <h3>تفعيل المصادقة الثنائية</h3>
                  <p>احمِ حسابك بطبقة أمان إضافية</p>
                </div>
                <label className="toggle-switch">
                  <input type="checkbox" />
                  <span className="toggle-slider"></span>
                </label>
              </div>
            </div>

            <div className="section-card danger-zone">
              <h2 className="section-title">
                <span className="title-icon">⚠️</span>
                منطقة الخطر
              </h2>
              
              <div className="danger-actions">
                <button className="btn-danger">
                  🗑️ حذف الحساب نهائياً
                </button>
                <p className="danger-warning">
                  هذا الإجراء لا يمكن التراجع عنه. سيتم حذف جميع بياناتك نهائياً.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'activity' && (
          <div className="profile-section">
            <div className="section-card">
              <h2 className="section-title">
                <span className="title-icon">📊</span>
                النشاط الأخير
              </h2>
              
              <div className="activity-timeline">
                <div className="activity-item">
                  <div className="activity-icon success">✓</div>
                  <div className="activity-content">
                    <h3>تم رفع 5 بطاقات جديدة</h3>
                    <p className="activity-time">منذ ساعتين</p>
                  </div>
                </div>

                <div className="activity-item">
                  <div className="activity-icon info">📝</div>
                  <div className="activity-content">
                    <h3>تم تحديث معلومات الملف الشخصي</h3>
                    <p className="activity-time">منذ 3 ساعات</p>
                  </div>
                </div>

                <div className="activity-item">
                  <div className="activity-icon success">✓</div>
                  <div className="activity-content">
                    <h3>تم تصدير مجموعة بيانات جديدة</h3>
                    <p className="activity-time">منذ يوم واحد</p>
                  </div>
                </div>

                <div className="activity-item">
                  <div className="activity-icon warning">⚡</div>
                  <div className="activity-content">
                    <h3>تم بدء معالجة دفعة جديدة</h3>
                    <p className="activity-time">منذ يومين</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;
