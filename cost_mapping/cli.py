"""Command-line trip economics and cost-surface tools."""
import argparse
import json
from . import __version__
from .economics import Gig, Assumptions, evaluate

def add_assumptions(parser):
    parser.add_argument('--cost-per-mile',type=float,default=.30,help='Vehicle operating cost; illustrative default 0.30')
    parser.add_argument('--target-hourly',type=float,default=20,help='Desired earnings after trip expenses')

def add_gig(parser):
    parser.add_argument('--name',default='Gig')
    parser.add_argument('--payout',type=float,required=True)
    parser.add_argument('--miles',type=float,required=True,help='Total distance including any return travel')
    parser.add_argument('--driving-minutes',type=float,required=True)
    for option in ('work-minutes','waiting-minutes','tolls','parking'):
        parser.add_argument('--'+option,type=float,default=0)
    add_assumptions(parser)

def parser():
    root=argparse.ArgumentParser(description='Compare trip expenses and earnings with explicit assumptions')
    root.add_argument('--version',action='version',version=__version__)
    commands=root.add_subparsers(dest='command',required=True)
    single=commands.add_parser('evaluate',help='Evaluate a gig')
    add_gig(single)
    compare=commands.add_parser('compare',help='Rank gigs from a CSV file')
    compare.add_argument('source')
    compare.add_argument('--sort',choices=['effective_hourly','net_earnings','surplus'],default='effective_hourly')
    add_assumptions(compare)
    scenarios=commands.add_parser('scenarios',help='Compare lower/base/higher driving cost and time')
    add_gig(scenarios)
    route=commands.add_parser('route',help='Estimate a route offline or request Google routing')
    route.add_argument('--origin',required=True,help='latitude,longitude')
    route.add_argument('--destination',required=True,help='latitude,longitude')
    route.add_argument('--provider',choices=['offline','google'],default='offline')
    route.add_argument('--round-trip',action='store_true')
    route.add_argument('--speed-mph',type=float,default=25)
    route.add_argument('--road-factor',type=float,default=1.3)
    route.add_argument('--avoid-tolls',action='store_true')
    route.add_argument('--max-requests',type=int,default=2)
    route.add_argument('--dry-run',action='store_true')
    return root

def gig_from_args(args):
    return Gig(**{field:getattr(args,field) for field in Gig.__dataclass_fields__})

def execute(args):
    if args.command=='route':
        from dataclasses import asdict
        from .geo import Point
        from .offline import estimate_route
        from .google import google_route
        from .collect import RequestBudget, round_trip
        from .units import miles, minutes
        origin,destination=Point.parse(args.origin),Point.parse(args.destination)
        count=2 if args.round_trip else 1
        budget=RequestBudget(args.max_requests)
        if count>budget.limit: raise ValueError('Request limit is smaller than the planned route count')
        if args.dry_run: return {'provider':args.provider,'requests':count if args.provider=='google' else 0,'round_trip':args.round_trip}
        provider=(lambda a,b: google_route(a,b,avoid_tolls=args.avoid_tolls)) if args.provider=='google' else (lambda a,b:estimate_route(a,b,speed_mph=args.speed_mph,road_factor=args.road_factor))
        result=round_trip(origin,destination,provider,budget=budget) if args.round_trip else budget.call(provider,origin,destination)
        return {**asdict(result),'miles':miles(result.meters,'meters'),'minutes':minutes(result.seconds,'seconds'),'requests':budget.used if args.provider=='google' else 0}
    if args.command=='scenarios':
        from .scenarios import sensitivity
        return sensitivity(gig_from_args(args),Assumptions(args.cost_per_mile,args.target_hourly))
    if args.command=='compare':
        from .imports import load_gigs
        assumptions=Assumptions(args.cost_per_mile,args.target_hourly)
        return sorted([evaluate(gig,assumptions) for gig in load_gigs(args.source)],key=lambda row:row[args.sort],reverse=True)
    if args.command=='evaluate':
        return evaluate(gig_from_args(args),Assumptions(args.cost_per_mile,args.target_hourly))
    raise ValueError('Unknown command')

def main(argv=None):
    root=parser()
    args=root.parse_args(argv)
    try:
        result=execute(args)
        if result is not None: print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
        return 0
    except BrokenPipeError:
        return 0
    except (ValueError,OSError) as error:
        root.exit(2,f'error: {error}\n')
