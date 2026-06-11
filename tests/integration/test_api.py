
import pytest
from datetime import datetime
from src.api.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


class TestAPIEndpoints:
    """API端点集成测试"""
    
    def test_root_endpoint(self):
        """测试根端点"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "domains" in data
    
    def test_domains_endpoint(self):
        """测试术数域列表端点"""
        response = client.get("/api/v1/analysis/domains")
        assert response.status_code == 200
        data = response.json()
        assert "domains" in data
        assert len(data["domains"]) == 7
    
    def test_engine_status_endpoint(self):
        """测试引擎状态端点"""
        response = client.get("/api/v1/analysis/status")
        assert response.status_code == 200
        data = response.json()
        assert "engines" in data
        assert len(data["engines"]) == 7
    
    def test_bazi_calc_endpoint(self):
        """测试八字计算端点"""
        response = client.post(
            "/api/v1/bazi/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "result" in data
        assert "reasoning_chain" in data
    
    def test_ziwei_calc_endpoint(self):
        """测试紫微计算端点"""
        response = client.post(
            "/api/v1/ziwei/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_qimen_calc_endpoint(self):
        """测试奇门遁甲计算端点"""
        response = client.post(
            "/api/v1/qimen/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_liuren_calc_endpoint(self):
        """测试大六壬计算端点"""
        response = client.post(
            "/api/v1/liuren/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_meihua_calc_endpoint(self):
        """测试梅花易数计算端点"""
        response = client.post(
            "/api/v1/meihua/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_liuyao_calc_endpoint(self):
        """测试六爻计算端点"""
        response = client.post(
            "/api/v1/liuyao/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_taiyi_calc_endpoint(self):
        """测试太乙数计算端点"""
        response = client.post(
            "/api/v1/taiyi/calc",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_comprehensive_analysis_endpoint(self):
        """测试综合分析端点"""
        response = client.post(
            "/api/v1/analysis/comprehensive",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京",
                "domains": ["bazi", "ziwei"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "results" in data
        assert "bazi" in data["results"]
        assert "ziwei" in data["results"]
    
    def test_comprehensive_all_domains(self):
        """测试综合分析所有术数域"""
        response = client.post(
            "/api/v1/analysis/comprehensive",
            json={
                "birth_date": "2000-01-01",
                "birth_time": "12:00",
                "timezone": "UTC+8",
                "location": "北京",
                "domains": ["bazi", "ziwei", "qimen", "liuren", "meihua", "liuyao", "taiyi"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["results"]) == 7
    
    def test_bazi_rules_endpoint(self):
        """测试八字规则端点"""
        response = client.get("/api/v1/bazi/rules")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
    
    def test_ziwei_stars_endpoint(self):
        """测试紫微星曜端点"""
        response = client.get("/api/v1/ziwei/stars")
        assert response.status_code == 200
        data = response.json()
        assert "main_stars" in data
        assert len(data["main_stars"]) == 14
    
    def test_ziwei_palaces_endpoint(self):
        """测试紫微宫位端点"""
        response = client.get("/api/v1/ziwei/palaces")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 12
