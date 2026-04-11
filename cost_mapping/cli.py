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
    return root

def gig_from_args(args):
    return Gig(**{field:getattr(args,field) for field in Gig.__dataclass_fields__})

def execute(args):
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
