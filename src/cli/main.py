
import click
from datetime import datetime
from typing import Optional

from ..engines import (
    BaziEngine, ZiweiEngine, QimenEngine, 
    LiurenEngine, MeihuaEngine, LiuyaoEngine, TaiyiEngine
)


@click.group()
@click.version_option(version="0.1.0", prog_name="mingli")
def cli():
    """MingLi AI Agent - 术数推理命理智能体命令行工具"""
    pass


@cli.command()
@click.option('--date', '-d', required=True, help='出生日期 (YYYY-MM-DD)')
@click.option('--time', '-t', required=True, help='出生时间 (HH:MM)')
@click.option('--timezone', '-tz', default='UTC+8', help='时区 (默认: UTC+8)')
@click.option('--location', '-l', default='北京', help='出生地点')
def bazi(date: str, time: str, timezone: str, location: str):
    """八字排盘计算"""
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
        engine = BaziEngine()
        result = engine.calculate(birth_date, time, timezone, location)
        
        if result.success:
            click.echo("\n" + "=" * 50)
            click.echo("八字排盘结果")
            click.echo("=" * 50)
            click.echo(f"\n四柱: {result.result['bazi_pillar']}")
            click.echo(f"日主: {result.result['daymaster']}")
            click.echo(f"\n五行分布:")
            for wuxing, count in result.result['wuxing'].items():
                click.echo(f"  {wuxing}: {count}")
            click.echo(f"\n纳音:")
            for pillar, nayin in result.result['nayin'].items():
                click.echo(f"  {pillar}: {nayin}")
            click.echo(f"\n置信度: {result.confidence}")
        else:
            click.echo(f"计算失败: {result.error}", err=True)
    except ValueError as e:
        click.echo(f"日期格式错误: {e}", err=True)


@cli.command()
@click.option('--date', '-d', required=True, help='出生日期 (YYYY-MM-DD)')
@click.option('--time', '-t', required=True, help='出生时间 (HH:MM)')
@click.option('--timezone', '-tz', default='UTC+8', help='时区')
@click.option('--location', '-l', default='北京', help='出生地点')
def ziwei(date: str, time: str, timezone: str, location: str):
    """紫微斗数排盘"""
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
        engine = ZiweiEngine()
        result = engine.calculate(birth_date, time, timezone, location)
        
        if result.success:
            click.echo("\n" + "=" * 50)
            click.echo("紫微斗数排盘结果")
            click.echo("=" * 50)
            click.echo(f"\n紫微宫: {result.result['ziwei_palace']}")
            click.echo(f"\n十二宫:")
            for palace, pos in result.result['palaces'].items():
                click.echo(f"  {palace}: {pos}")
            click.echo(f"\n置信度: {result.confidence}")
        else:
            click.echo(f"计算失败: {result.error}", err=True)
    except ValueError as e:
        click.echo(f"日期格式错误: {e}", err=True)


@cli.command()
@click.option('--date', '-d', required=True, help='出生日期 (YYYY-MM-DD)')
@click.option('--time', '-t', required=True, help='出生时间 (HH:MM)')
@click.option('--timezone', '-tz', default='UTC+8', help='时区')
@click.option('--location', '-l', default='北京', help='出生地点')
def qimen(date: str, time: str, timezone: str, location: str):
    """奇门遁甲排盘"""
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
        engine = QimenEngine()
        result = engine.calculate(birth_date, time, timezone, location)
        
        if result.success:
            click.echo("\n" + "=" * 50)
            click.echo("奇门遁甲排盘结果")
            click.echo("=" * 50)
            click.echo(f"\n时辰干支: {result.result['hour_ganzhi']}")
            click.echo(f"盘类型: {result.result['pan_type']}")
            click.echo(f"\n九星:")
            for star, pos in result.result['jiuxing'].items():
                click.echo(f"  {star}: {pos}")
            click.echo(f"\n置信度: {result.confidence}")
        else:
            click.echo(f"计算失败: {result.error}", err=True)
    except ValueError as e:
        click.echo(f"日期格式错误: {e}", err=True)


@cli.command()
@click.option('--date', '-d', required=True, help='出生日期 (YYYY-MM-DD)')
@click.option('--time', '-t', required=True, help='出生时间 (HH:MM)')
@click.option('--timezone', '-tz', default='UTC+8', help='时区')
@click.option('--location', '-l', default='北京', help='出生地点')
@click.option('--domains', default='bazi,ziwei', help='术数域 (逗号分隔)')
def analyze(date: str, time: str, timezone: str, location: str, domains: str):
    """综合命理分析"""
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
        domain_list = domains.split(',')
        
        engines = {
            "bazi": (BaziEngine(), "八字"),
            "ziwei": (ZiweiEngine(), "紫微"),
            "qimen": (QimenEngine(), "奇门"),
            "liuren": (LiurenEngine(), "大六壬"),
            "meihua": (MeihuaEngine(), "梅花"),
            "liuyao": (LiuyaoEngine(), "六爻"),
            "taiyi": (TaiyiEngine(), "太乙")
        }
        
        click.echo("\n" + "=" * 60)
        click.echo("综合命理分析结果")
        click.echo("=" * 60)
        
        for domain in domain_list:
            domain = domain.strip()
            if domain in engines:
                engine, name = engines[domain]
                result = engine.calculate(birth_date, time, timezone, location)
                
                if result.success:
                    click.echo(f"\n【{name}】")
                    if domain == "bazi":
                        click.echo(f"  四柱: {result.result.get('bazi_pillar', '')}")
                        click.echo(f"  日主: {result.result.get('daymaster', '')}")
                    elif domain == "ziwei":
                        click.echo(f"  紫微宫: {result.result.get('ziwei_palace', '')}")
                    elif domain == "qimen":
                        click.echo(f"  盘类型: {result.result.get('pan_type', '')}")
                    elif domain == "meihua":
                        shang = result.result.get('shang_gua', {}).get('name', '')
                        xia = result.result.get('xia_gua', {}).get('name', '')
                        click.echo(f"  卦象: {shang}{xia}")
                else:
                    click.echo(f"\n【{name}】计算失败: {result.error}")
        
    except ValueError as e:
        click.echo(f"日期格式错误: {e}", err=True)


@cli.command()
def domains():
    """列出所有支持的术数域"""
    click.echo("\n支持的术数域:")
    click.echo("  bazi   - 八字（四柱）")
    click.echo("  ziwei  - 紫微斗数")
    click.echo("  qimen  - 奇门遁甲")
    click.echo("  liuren - 大六壬")
    click.echo("  meihua - 梅花易数")
    click.echo("  liuyao - 六爻")
    click.echo("  taiyi  - 太乙数")


@cli.command()
@click.option('--date', '-d', required=True, help='出生日期 (YYYY-MM-DD)')
@click.option('--gender', '-g', default='男', help='性别 (男/女)')
@click.option('--age', '-a', default=30, help='当前年龄')
def dayun(date: str, gender: str, age: int):
    """计算大运流年"""
    try:
        birth_date = datetime.strptime(date, "%Y-%m-%d")
        engine = BaziEngine()
        result = engine.calculate_dayun_liunian(birth_date, gender, age)
        
        if result['success']:
            click.echo("\n" + "=" * 50)
            click.echo("大运流年分析")
            click.echo("=" * 50)
            
            dayun_info = result.get('dayun', {})
            click.echo(f"\n大运方向: {dayun_info.get('direction', '')}")
            click.echo(f"起运年龄: {dayun_info.get('start_age', '')}岁")
            
            click.echo("\n大运序列:")
            for dy in dayun_info.get('dayun_list', []):
                click.echo(f"  第{dy['step']}步: {dy['ganzhi']} ({dy['age_range']}岁)")
            
            click.echo("\n流年:")
            for ln in result.get('liunian', []):
                click.echo(f"  {ln['year']}年 ({ln['age']}岁): {ln['ganzhi']}")
            
            current = result.get('current_dayun', {})
            if current:
                click.echo(f"\n当前大运: {current.get('ganzhi', '')} ({current.get('age_range', '')}岁)")
        else:
            click.echo(f"计算失败: {result.get('error', '')}", err=True)
    except ValueError as e:
        click.echo(f"日期格式错误: {e}", err=True)


if __name__ == '__main__':
    cli()
